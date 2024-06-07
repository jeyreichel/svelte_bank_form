<script lang="ts">
  import { tooltipElement } from "$lib/jscomponent/tooltip.js";

  export let values = [],
    choice,
    tooltip = "",
    name = "group_1";
</script>

{#each values as value, i}
  <div
    class:grid={tooltip !== "" && i === values.length - 1}
    class:grid-cols-12={tooltip !== "" && i === values.length - 1}
  >
    <div
      class="flex items-center pl-4 rounded cursor-pointer field-radio"
      class:border-gray-300={choice !== value.value}
      class:border={choice !== value.value}
      class:border-purple={choice === value.value}
      class:border-4={choice === value.value}
      class:col-span-10={tooltip !== "" && i === values.length - 1}
    >
      <input
        bind:group={choice}
        id="id_{name}"
        type="radio"
        value={value.value}
        {name}
        class="w-4 h-4 bg-gray-100 border-gray-300 cursor-pointer"
      />
      <label
        for="id_{value.value}"
        class="w-full py-4 ml-2 text-sm cursor-pointer
        font-medium text-gray-900">{value.label}</label
      >
    </div>
    {#if tooltip && i === values.length - 1}
      <div
        class="self-center text-center cursor-pointer"
        class:col-span-2={true}
      >
        <span use:tooltipElement title={tooltip} class="bi bi-info-circle"
        ></span>
      </div>
    {/if}
  </div>
{/each}

<style>
  input {
    color: var(--color-theme-2);
  }

  input:focus {
    --tw-ring-color: none;
  }

  .border-purple {
    border: 1px solid var(--color-theme-2);
  }

  .field-radio {
    display: flex;
    align-items: center;
    background-color: #fff;
    border-radius: var(--border-radius);
    height: 60px;
    box-shadow: 0 4px 8px rgba(172, 186, 200, 0.1);
  }
</style>
