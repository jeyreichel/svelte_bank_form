<script lang="ts">
  import SelectComponent from "$lib/components/SelectComponent.svelte";
  import StepComponent from "$lib/components/StepComponent.svelte";
  import Radio from "$lib/components/Radio.svelte";
  import CustomInput from "$lib/components/CustomInput.svelte";
  import DateInput from "$lib/components/DateInput.svelte";
  import Ajv from "ajv";
  import addFormats from "ajv-formats";
  import localize from "ajv-i18n";
  import { profession, travaux_manuels } from "../../data/select.js";
  import ForwardButton from "$lib/components/ForwardButton.svelte";
  import { changeStep, getTokenWithExpiry } from "$lib/utils.js";
  import {
    DeplacementsPro,
    Genre,
    Profession,
    TravauxManuels,
    type Assure,
    type Simulation,
  } from "$lib/api/models.js";
  import { onMount } from "svelte";
  import SelectComponentSlots from "$lib/components/SelectComponentSlots.svelte";

  const ajv = new Ajv({ allErrors: true });
  addFormats(ajv);

  export let step: number, simulation: Partial<Simulation>;

  let next_ok = false;

  const nombre_emprunteurs: number = getTokenWithExpiry("nombre_emprunteurs");
  let data: Array<Partial<Assure>> = [{}],
    errors: Array<Object> = [];

  // let zipCode = "";
  // let city = "";

  onMount(() => {
    if (simulation.assures) {
      data = simulation.assures;
    } else {
      for (let i = 0; i < nombre_emprunteurs; i++) {
        data = [...data, {}];
        errors = [...errors, {}];
      }
    }
  });

  let civilite_options = [
    { text: "Madame", value: Genre.FEMME },
    { text: "Monsieur", value: Genre.HOMME },
  ];

  let fumeur_options = [
    { text: "Non Fumeur", value: false },
    { text: "Fumeur", value: true },
  ];

  let deplacements_pro_options = [
    { text: "Aucun déplacement", value: DeplacementsPro.AUCUN },
    { text: "Moins de 20 000km/an", value: DeplacementsPro.MOINS_20000 },
    { text: "Plus de 20 000km", value: DeplacementsPro.PLUS_20000 },
  ];

  const schema = {
    type: "object",
    properties: {
      nom: { type: "string", minLength: 1 },
      prenom: { type: "string", minLength: 1 },
      adresse: { type: "string", minLength: 1 },
      ville: { type: "string", minLength: 1 },
      code_postal: {
        type: "string",
        pattern: "^\\d{5}$",
      },
      telephone: {
        type: "string",
        pattern:
          "^(0|\\+33|0033)[ ][0-9][ ][0-9]{2}[ ][0-9]{2}[ ][0-9]{2}[ ][0-9]{2}$",
        maxLength: 17,
      },
      email: { type: "string", format: "email" },
      date_naissance: { type: "object" },
      profession: { enum: Object.values(Profession) },
      travaux_manuels: { enum: Object.values(TravauxManuels) },
      quotite: { type: "integer", minimum: 0, maximum: 100 },
    },
    required: [
      "nom",
      "prenom",
      "adresse",
      "code_postal",
      "telephone",
      "ville",
      "date_naissance",
      "profession",
      "travaux_manuels",
      "quotite",
    ],
  };
  const validate = ajv.compile(schema);

  function validate_data(data: Array<Partial<Assure>>) {
    next_ok = true;
    for (let i = 0; i < data.length; i++) {
      errors[i] = {};
      const valid = validate(data[i]);
      localize.fr(validate.errors);
      if (!valid) {
        next_ok = false;
        validate.errors.forEach((elem) => {
          if (elem.instancePath === "/email") {
            elem.message = "Veuillez entrer une adresse e-mail valide.";
          }
          if (elem.instancePath === "/code_postal") {
            elem.message =
              "Veuillez entrer un code postal valide (format: 5 chiffres).";
          }
          if (elem.instancePath === "/telephone") {
            elem.message = "Veuillez entrer un numéro de téléphone valide.";
          }
          if (elem.instancePath === "/date_naissance") {
            if (elem.keyword === "formatMaximum") {
              elem.message =
                "Le titulaire du contrat doit avoir plus de 18 ans";
            } else if (elem.keyword === "format") {
              elem.message = "Veuillez entrer une date valide";
            }
          }
          elem.message = elem.message.replace("=", "");
          elem.message = elem.message.replace("<", "inférieur à");
          elem.message = elem.message.replace(">", "supérieur à");
          elem.message = elem.message.replace(/./, (c) => c.toUpperCase());
          errors[i][elem.instancePath.substring(1)] = {
            type: elem.keyword,
            message: elem.message,
          };
          // console.log(errors);
        });
      }
    }
  }

  $: if (data) {
    validate_data(data);
  }

  function updateSimulation(data: Array<Assure>) {
    let assures: Array<Assure> = [];
    data.forEach((assure) => assures.push(assure));
    simulation = { ...simulation, assures };
    step = changeStep(step);
  }

  function changePhone(val, i) {
    let phone = val.replace(/ /g, ""); // Remove spaces from input
    let phoneNumber =
      "+33 " +
      phone.substring(3, 4) +
      " " +
      phone.substring(4, 6) +
      " " +
      phone.substring(6, 8) +
      " " +
      phone.substring(8, 10) +
      " " +
      phone.substring(10, 12);
    data[i]["telephone"] = phoneNumber;
  }

  // async function validateAddress() {
  //   const response = await fetch(
  //     `https://maps.googleapis.com/maps/api/geocode/json?address=${data[i]["address"]}&components=france:FR&key=<YOUR_API_KEY>`
  //   );
  //   const data = await response.json();

  //   if (data.status === "OK") {
  //     const addressComponents = data.results[0].address_components;

  //     zipCode = addressComponents.find((component) =>
  //       component.types.includes("postal_code")
  //     ).long_name;
  //     city = addressComponents.find((component) =>
  //       component.types.includes("locality")
  //     ).long_name;
  //   } else {
  //     console.error("Invalid address");
  //   }
  // }
</script>

<StepComponent bind:step forward={next_ok} form>
  <div slot="title">Votre profil emprunteur</div>
  <div slot="description">
    Les tarifs proposé par les assureurs changent en fonction de votre profil,
    nous avons besoin d'en savoir plus !
  </div>
  <div slot="body">
    {#each data as assure, i}
      <h1 class="mb-12 text-left font-extrabold text-gray-900">
        {#if i == 0}
          Vous
        {:else}
          Votre co-emprunteur
        {/if}
      </h1>
      <!-- {simulation.prets?.map((item) => {
        console.log(
          typeof item.taux,
          typeof item.montant,
          typeof item.premiere_mensualite
        );
      })} -->
      <div class="mb-10">
        <div>
          <div class="grid grid-cols-1 md:gap-16 gap-12 mb-12">
            <CustomInput
              type="number"
              required
              min="10"
              max="200"
              id="quotite"
              bind:value={data[i]["quotite"]}
              valid={errors[i]["quotite"]}
              tooltip="Il s'agit de la proportion de la mensualité du prêt que vous souhaitez assurer"
            >
              <div slot="label">Quotité à assurer</div>
              <div slot="suffix">%</div>
            </CustomInput>
          </div>
          <div class="grid grid-cols-3 md:gap-16 gap-12 mb-12">
            <SelectComponentSlots
              bind:value={data[i]["genre"]}
              label="Civilité"
              id="genre"
            >
              <option value={0}>Allez-y et choisissez...</option>
              {#each civilite_options as item}
                <option value={item.value}>{item.text}</option>
              {/each}
            </SelectComponentSlots>
            <CustomInput
              type="text"
              required
              id="nom"
              bind:value={data[i]["nom"]}
              valid={errors[i]["nom"]}
              dont_accept_figures={true}
            >
              <div slot="label">Nom</div>
            </CustomInput>
            <CustomInput
              type="text"
              required
              id="prenom"
              bind:value={data[i]["prenom"]}
              valid={errors[i]["prenom"]}
              dont_accept_figures={true}
            >
              <div slot="label">Prénom</div>
            </CustomInput>
          </div>
          <div class="grid grid-cols-2 md:gap-16 gap-12 mb-12">
            <DateInput
              id="date_naissance"
              bind:date={data[i]["date_naissance"]}
              valid={errors[i]["date_naissance"]}
              >Date de naissance
            </DateInput>
            <SelectComponentSlots
              id="profession"
              bind:value={data[i]["profession"]}
              label="Profession"
              tooltip="Si votre profession n'est pas présente dans la liste, choisissez celle qui s'en approche le plus"
            >
              <option value={0}>Allez-y et choisissez...</option>
              {#each profession as item}
                <option value={item.value}>{item.text}</option>
              {/each}
            </SelectComponentSlots>
          </div>
          <div class="grid grid-cols-2 md:gap-16 gap-12 mb-12">
            <CustomInput
              type="text"
              required
              id="adresse"
              bind:value={data[i]["adresse"]}
              valid={errors[i]["adresse"]}
            >
              <div slot="label">Adresse</div>
            </CustomInput>
            <div class="grid grid-cols-2 gap-2">
              <CustomInput
                type="text"
                required
                id="code_postal"
                bind:value={data[i]["code_postal"]}
                valid={errors[i]["code_postal"]}
                dont_accept_string={true}
              >
                <div slot="label">Code postal</div>
              </CustomInput>
              <CustomInput
                type="text"
                required
                id="ville"
                bind:value={data[i]["ville"]}
                valid={errors[i]["ville"]}
              >
                <div slot="label">Ville</div>
              </CustomInput>
            </div>
            <CustomInput
              type="text"
              required
              id="telephone"
              bind:value={data[i]["telephone"]}
              valid={errors[i]["telephone"]}
              on:input={(e) => changePhone(e.target.value, i)}
              dont_accept_string={true}
            >
              <div slot="label">Téléphone</div>
            </CustomInput>
            <CustomInput
              type="text"
              required
              id="email"
              bind:value={data[i]["email"]}
              valid={errors[i]["email"]}
            >
              <div slot="label">E-mail</div>
            </CustomInput>
          </div>
          <div class="grid grid-cols-3 md:gap-12 gap-2 mb-12">
            <SelectComponentSlots
              id="fumeur"
              bind:value={data[i]["fumeur"]}
              label="Statut fumeur"
              tooltip="L'assureur vous considère comme fumeur si vous n'avez fumé dans les 24 mois"
            >
              <option value={0}>Allez-y et choisissez...</option>
              {#each fumeur_options as item}
                <option value={item.value}>{item.text}</option>
              {/each}
            </SelectComponentSlots>
            <SelectComponentSlots
              id="travaux"
              bind:value={data[i]["deplacements_pro"]}
              label="Déplacements professionels"
              tooltip="Il s'agit des déplacements que vous effectuez dans le cadre de votre travail, sans prendre en compte les trajets domicile-travail."
            >
              <option value={0}>Allez-y et choisissez...</option>
              {#each deplacements_pro_options as item}
                <option value={item.value}>{item.text}</option>
              {/each}
            </SelectComponentSlots>
            <SelectComponentSlots
              id="travaux"
              bind:value={data[i]["travaux_manuels"]}
              label="Activité professionelle manuelle"
              tooltip="Un travail manuel moyen ou important concerne l'utilisation d'outillages mécanique lourd, à bois, avec utilisation occasionnelle d'explosifs et/ou d'échafaudages"
            >
              <option value={0}>Allez-y et choisissez...</option>
              {#each travaux_manuels as item}
                <option value={item.value}>{item.text}</option>
              {/each}
            </SelectComponentSlots>
          </div>
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
      <ForwardButton on:click={(_) => updateSimulation(data)} />
    </div>
  </div>
</StepComponent>
