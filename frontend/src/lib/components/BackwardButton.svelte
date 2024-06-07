<script>
  import Button from "$lib/components/Button.svelte";
  import { changeStep } from "$lib/utils.js";

  export let step;
</script>

{#if step > 1}
  <Button
    on:click={() => {
      step = changeStep(step, true);
    }}
  >
    <i class="bi bi-arrow-left"></i> Retour
  </Button>
{/if}
