<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import Results from "$lib/components/Results.svelte";
  import Loading from "$lib/components/Loading.svelte";
  import { onMount } from "svelte";

  let id_simulation: string | null;

  onMount(() => {
    id_simulation = $page.url.searchParams.get("simulation_id");
    if (!id_simulation) goto("/");
  });
</script>

{#if !id_simulation}
  <Loading />
{:else}
  <Results bind:id_simulation />
{/if}
