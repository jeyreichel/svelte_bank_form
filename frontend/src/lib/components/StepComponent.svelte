<script>
  // @ts-nocheck

  import BackwardButton from "$lib/components/BackwardButton.svelte";

  export let step,
    buttons_up = false,
    forward = false,
    end = false;
  export let form = false,
    flying = true,
    overflow_y = true;
</script>

<div
  class="text-left inline"
  class:bg-white={form}
  class:p-12={form}
  class:mt-12={form}
  class:rounded-md={form}
  class:step_component={flying}
  class:overflow-y-auto={overflow_y}
>
  {#if buttons_up}
    <div
      class:text-center={forward}
      class:grid={forward}
      class:grid-cols-2={forward}
      class:gap-10={forward}
    >
      <div class="mt-4">
        <BackwardButton bind:step />
      </div>
      {#if $$slots.button && forward}
        <slot name="button"></slot>
      {/if}
    </div>
  {/if}
  {#if $$slots.title}
    <h1 class="mb-4 text-left font-extrabold text-gray-900 md:text-xl">
      <slot name="title"></slot>
    </h1>
  {/if}
  {#if $$slots.description}
    <p class="text-left text-gray-900">
      <slot name="description"></slot>
    </p>
  {/if}

  {#if $$slots.up}
    <slot name="up"></slot>
  {/if}

  {#if $$slots.body}
    <slot name="body"></slot>
  {/if}
  {#if !buttons_up}
    <div class:text-center={forward | end} class="flex justify-between">
      <div class="mt-4">
        <BackwardButton bind:step />
      </div>
      <slot name="button"></slot>
    </div>
  {/if}
</div>

<style>
  @media (min-width: 480px) {
    .step_component {
      animation: animate 0.7s ease forwards;
    }
  }

  @keyframes animate {
    0% {
      transform: translateX(50%);
    }
    100% {
      transform: translateX(0%);
    }
  }
</style>
