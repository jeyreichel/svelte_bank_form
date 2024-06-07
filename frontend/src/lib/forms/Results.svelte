<script lang="ts">
  import type { Simulation } from "$lib/api/models";
  import Results from "$lib/components/Results.svelte";

  export let step: number, simulation: Simulation;
</script>

<Results bind:step bind:simulation />
