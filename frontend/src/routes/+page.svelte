<script lang="ts">
  import ProgressBar from "$lib/components/ProgressBar.svelte";

  import ObjetDemande from "$lib/forms/ObjetDemande.svelte";
  import Banque from "$lib/forms/Banque.svelte";
  import ObjetPret from "$lib/forms/ObjetPret.svelte";
  import NbEmprunteurs from "$lib/forms/NbEmprunteurs.svelte";
  import Prets from "$lib/forms/Prets.svelte";
  import Assures from "$lib/forms/Assures.svelte";
  import { clear_storage } from "$lib/config";
  import Results from "$lib/forms/Results.svelte";
  import { onMount } from "svelte";
  import type { Simulation } from "$lib/api/models";

  let step = 1;
  let simulation: Partial<Simulation>;

  onMount(() => {
    if (clear_storage) {
      localStorage.clear();
    }
  });
</script>

<svelte:head>
  <title>Omeros</title>
  <meta
    name="description"
    content="Optimisez votre assurance emprunteur et économisez"
  />
</svelte:head>
<ProgressBar {step}></ProgressBar>

<div class="section">
  {#if step === 1}
    <ObjetDemande bind:step bind:simulation></ObjetDemande>
  {:else if step === 2}
    <Banque bind:step bind:simulation></Banque>
  {:else if step === 3}
    <ObjetPret bind:step bind:simulation></ObjetPret>
  {:else if step === 4}
    <NbEmprunteurs bind:step></NbEmprunteurs>
  {:else if step === 5}
    <Prets bind:step bind:simulation></Prets>
  {:else if step === 6}
    <Assures bind:step bind:simulation></Assures>
  {:else}
    <Results bind:step bind:simulation></Results>
  {/if}
</div>

<style lang="postcss">
  .section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 0.6;
  }
</style>
