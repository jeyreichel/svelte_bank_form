<script lang="ts">
  import StepComponent from "$lib/components/StepComponent.svelte";
  import Button from "$lib/components/Button.svelte";
  import CustomInput from "$lib/components/CustomInput.svelte";
  import Ajv from "ajv";
  import localize from "ajv-i18n";
  import addFormats from "ajv-formats";
  import { type_pret } from "../../data/select.js";
  import DateInput from "$lib/components/DateInput.svelte";
  import SelectComponentSlots from "$lib/components/SelectComponentSlots.svelte";
  import ForwardButton from "$lib/components/ForwardButton.svelte";
  import { changeStep } from "$lib/utils.js";
  import { TypePret, type Pret, type Simulation } from "$lib/api/models.js";

  const ajv = new Ajv({ allErrors: true });
  addFormats(ajv);

  export let step: number;
  export let simulation: Partial<Simulation>;

  let errors = [{}];
  let data: Array<Partial<Pret>> = simulation.prets ?? [{}];

  let next_ok = false;
  let montantValue: String = simulation.montantValue ?? "",
    tauxValue: String = simulation.tauxValue ?? "";

  let taux_variable_options = [
    { text: "Taux fixe", value: false },
    { text: "Taux variable", value: true },
  ];

  const schema = {
    type: "object",
    properties: {
      type_pret: { enum: Object.values(TypePret) },
      montant: {
        type: "number",
        minimum: 30000,
        maximum: 4000000000,
      },
      taux: {
        type: "number",
        minimum: 0,
        maximum: 100,
      },
      taux_variable: { type: "boolean" },
      premiere_mensualite: { type: "object" },
      duree: { type: "integer", minimum: 1, maximum: 400 },
    },

    required: [
      "type_pret",
      "montant",
      "taux",
      "taux_variable",
      "premiere_mensualite",
      "duree",
    ],
  };

  const validate = ajv.compile(schema);

  function changeTaux(val, i) {
    data[i]["taux"] = parseFloat(val.replace(/[,]+/g, "."));
    let taux = tauxValue.replace(/(\d)(?=[.,\d])/g, "$1 "); // Add space after a digit if followed by a dot, comma, or digit
    taux = taux.replace(/[^\d.,]/g, ""); // Remove all characters except digits, dot, and comma
    taux = taux.replace(/[.,](?=.*[.,])/g, ""); // Remove additional dots or commas except the first one
    tauxValue = taux;
  }

  function changeMontant(val, i) {
    data[i]["montant"] = parseFloat(val.replace(/\s+/g, ""));
    let array = [];
    let montant = montantValue.replace(/ /g, "");
    for (let i = 0, len = montant.length; i < len; i += 3) {
      array.push(montant.substr(i, 3));
    }
    montantValue = array.join(" ");
  }

  function validate_data(data: Array<Partial<Pret>>) {
    next_ok = true;
    for (let pretId = 0; pretId < data.length; pretId++) {
      errors[pretId] = {};
      const valid = validate(data[pretId]);
      localize.fr(validate.errors);
      if (!valid) {
        next_ok = false;
        validate.errors.forEach((elem) => {
          if (elem.instancePath === "/premiere_mensualite") {
            if (elem.keyword === "format") {
              elem.message = "Veuillez entrer une date valide";
            }
          }
          elem.message = elem.message.replace("=", "");
          elem.message = elem.message.replace("<", "inférieur à");
          elem.message = elem.message.replace(">", "supérieur à");
          elem.message = elem.message.replace(/./, (c) => c.toUpperCase());
          errors[pretId][elem.instancePath.substring(1)] = {
            type: elem.keyword,
            message: elem.message,
          };
        });
      }
    }
  }

  $: if (data) {
    validate_data(data);
  }

  function addPret() {
    data = [...data, {}];
    errors = [...errors, {}];
  }

  function removePret() {
    data.splice(-1);
    errors.splice(-1);
    // Force Svelte reactiveness
    data = data;
    errors = errors;
  }
  function updateSimulation(data, montantValue, tauxValue) {
    let prets: Array<Pret> = [];
    data.forEach((pret: Pret) => prets.push(pret));
    simulation = { ...simulation, prets, montantValue, tauxValue };
    step = changeStep(step);
  }
</script>

<StepComponent bind:step forward={next_ok} form>
  <div slot="title">Vos prêts</div>
  <div slot="description">
    Vous pouvez renseigner ici les prêts immobiliers que vous souhaitez assurer.
  </div>
  <div slot="body">
    {#each data as pret, i}
      <div
        class:my-10={i + 1 !== data.length}
        class:mt-10={i + 1 === data.length}
        class:mb-5={i + 1 === data.length}
      >
        <h2 class="mb-12 text-left font-extrabold text-gray-900">
          Prêt n°{i + 1}
        </h2>
        <div class="grid md:grid-cols-1 gap-16 mb-14">
          <SelectComponentSlots
            id="type_pret"
            bind:value={data[i]["type_pret"]}
            valid={errors[i]["type_pret"]}
            label="Type de prêt"
          >
            <option value={0}>Allez-y et choisissez...</option>
            {#each type_pret as item}
              <option value={item.value}>{item.text}</option>
            {/each}
          </SelectComponentSlots>
        </div>
        <div class="grid md:grid-cols-2 gap-16 mb-14">
          <CustomInput
            type="text"
            required
            id="montant_pret"
            bind:value={montantValue}
            valid={errors[i]["montant"]}
            on:input={(e) => changeMontant(e.target.value, i)}
            dont_accept_string={true}
          >
            <div slot="label">Montant emprunté</div>
            <div slot="suffix">€</div>
          </CustomInput>
          <DateInput
            id="date_mensualite"
            bind:date={data[i]["premiere_mensualite"]}
            valid={errors[i]["premiere_mensualite"]}
            only_month={true}
          >
            Date de première mensualité
          </DateInput>
        </div>

        <div class="grid md:grid-cols-2 gap-16 mb-14">
          <CustomInput
            type="text"
            required
            min="0"
            id="taux_pret"
            bind:value={tauxValue}
            valid={errors[i]["taux"]}
            on:input={(e) => changeTaux(e.target.value, i)}
            dont_accept_space={true}
          >
            <div slot="label">Taux</div>
            <div slot="suffix">%</div>
          </CustomInput>
          <SelectComponentSlots
            id="taux_variable"
            bind:value={data[i]["taux_variable"]}
            label="Type de taux"
          >
            <option value={0}>Allez-y et choisissez...</option>
            {#each taux_variable_options as item}
              <option value={item.value}>{item.text}</option>
            {/each}
          </SelectComponentSlots>
        </div>

        <div class="grid md:grid-cols-2 gap-16 mb-14">
          <CustomInput
            type="number"
            required
            min="1"
            id="ans"
            bind:value={data[i]["duree"]}
            valid={errors[i]["duree"]}
            dont_accept_figures={true}
          >
            <div slot="label">Durée totale</div>
            <div slot="suffix">mois</div>
          </CustomInput>
          <SelectComponentSlots
            id="dont_differe"
            bind:value={data[i]["differe"]}
            label="Dont différé"
          >
            <option value={0}>Sans différé</option>
            {#each Array(24) as _, i}
              <option value={i + 1}>{i + 1} mois</option>
            {/each}
          </SelectComponentSlots>
        </div>

        {#if i === data.length - 1 && i !== 0}
          <Button inversed on:click={() => removePret()}
            ><i class="'bi bi-x-circle text-red-400"></i> Supprimer ce prêt
          </Button>
        {/if}
        <div class="text-center" class:mt-4={data.length > 0}>
          {#if i < 2 && i === data.length - 1}
            <Button inversed on:click={() => addPret()}
              ><i class="'bi bi-plus-circle"></i><span> </span> Ajouter un prêt
            </Button>
          {/if}
        </div>
      </div>
    {/each}
  </div>
  <div slot="button">
    <div
      class="mt-4"
      class:pointer-events-none={!next_ok}
      class:opacity-50={!next_ok}
    >
      <ForwardButton
        on:click={(_) => updateSimulation(data, montantValue, tauxValue)}
      />
    </div>
  </div>
</StepComponent>
