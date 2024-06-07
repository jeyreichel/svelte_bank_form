<script lang="ts">
  import Card from "$lib/components/Card.svelte";
  import HouseImage from "$lib/images/step1/house.png";
  import Change from "$lib/images/step1/change.png";
  import Notebook from "$lib/images/step1/notebook.png";
  import StepComponent from "$lib/components/StepComponent.svelte";
  import { changeStep } from "$lib/utils.js";
  import { ObjetDemande, type Simulation } from "$lib/api/models";

  export let step: number;
  export let simulation: Partial<Simulation>;

  function updateSimulation(data: Partial<Simulation>) {
    simulation = { ...simulation, ...data };
    step = changeStep(step);
  }

  const objet_demande_options = [
    {
      text: "Un nouveau prêt",
      image: HouseImage,
      objet_demande: ObjetDemande.NOUVEAU_PRET,
    },
    {
      text: "Un changement d'assurance",
      image: Change,
      objet_demande: ObjetDemande.CHANGEMENT_ASSURANCE,
    },
    {
      text: "Une renégociation",
      image: Notebook,
      objet_demande: ObjetDemande.RENEGOCIATION,
    },
  ];
</script>

<StepComponent bind:step>
  <div slot="title">Vous souhaitez une assurance pour :</div>
  <div slot="body">
    <div class="grid md:grid-cols-3 gap-4 text-center">
      {#each objet_demande_options as objet_demande}
        <Card
          image={objet_demande.image}
          alt=""
          on:click={() =>
            updateSimulation({ objet_demande: objet_demande.objet_demande })}
        >
          <div slot="description">{objet_demande.text}</div>
        </Card>
      {/each}
    </div>
  </div>
</StepComponent>
