<script lang="ts">
  import Card from "$lib/components/Card.svelte";
  import Profil from "$lib/images/step4/profil.png";
  import Profil_2 from "$lib/images/step4/profil-2.png";
  import StepComponent from "$lib/components/StepComponent.svelte";
  import { changeStep, setTokenWithExpiry } from "$lib/utils.js";

  export let step: number;

  function saveEmprunteurs(nombre_emprunteurs: number) {
    setTokenWithExpiry("nombre_emprunteurs", nombre_emprunteurs.toString());
    step = changeStep(step);
  }

  const nombre_emprunteurs_options = [
    {
      nombre_emprunteurs: 1,
      text: "Vous",
      image: Profil,
    },
    {
      nombre_emprunteurs: 2,
      text: "Vous et votre co-emprunteur",
      image: Profil_2,
    },
  ];
</script>

<StepComponent bind:step>
  <div slot="title">Personne(s) à assurer</div>
  <div slot="body">
    <div class="grid md:grid-cols-2 gap-4 text-center">
      {#each nombre_emprunteurs_options as nombre_emprunteurs}
        <Card
          image={nombre_emprunteurs.image}
          alt={nombre_emprunteurs.text}
          on:click={() =>
            saveEmprunteurs(nombre_emprunteurs.nombre_emprunteurs)}
        >
          <div slot="description">{nombre_emprunteurs.text}</div>
        </Card>
      {/each}
    </div>
  </div>
</StepComponent>
