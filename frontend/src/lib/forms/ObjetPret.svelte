<script lang="ts">
  import Card from "$lib/components/Card.svelte";
  import Rent from "$lib/images/step3/rent.png";
  import Maison from "$lib/images/step3/maison.png";
  import Plage from "$lib/images/step3/plage.png";
  import StepComponent from "$lib/components/StepComponent.svelte";
  import { changeStep } from "$lib/utils.js";
  import { ObjetPret, type Simulation } from "$lib/api/models";

  export let step: number;
  export let simulation: Partial<Simulation>;

  function updateSimulation(data: Partial<Simulation>) {
    simulation = { ...simulation, ...data };
    step = changeStep(step);
  }

  const objet_pret_options = [
    {
      objet_pret: ObjetPret.RESIDENCE_PRINCIPALE,
      text: "Votre résidence principale",
      image: Maison,
    },
    {
      objet_pret: ObjetPret.RESIDENCE_SECONDAIRE,
      text: "Une résidence secondaire",
      image: Plage,
    },
    {
      objet_pret: ObjetPret.INVESTISSEMENT_LOCATIF,
      text: "Un investissement locatif",
      image: Rent,
    },
  ];
</script>

<StepComponent bind:step>
  <div slot="title">Objet du prêt</div>
  <div slot="body">
    <div class="grid md:grid-cols-3 gap-4 text-center">
      {#each objet_pret_options as objet_pret}
        <Card
          image={objet_pret.image}
          alt=""
          on:click={() =>
            updateSimulation({ objet_pret: objet_pret.objet_pret })}
        >
          <div slot="description">{objet_pret.text}</div>
        </Card>
      {/each}
    </div>
  </div>
</StepComponent>
