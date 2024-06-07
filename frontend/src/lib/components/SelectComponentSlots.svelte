<script>
  import { tooltipElement } from "$lib/jscomponent/tooltip.js";

  export let value,
    id,
    label,
    tooltip = "";
</script>

<div class:grid={tooltip !== ""} class:grid-cols-12={tooltip !== ""}>
  <label
    for={id}
    class="absolute md:text-xl text-gray-500 duration-300
                               transform -translate-y-6 translate-x-4 scale-75 origin-[0] peer-focus:left-0 peer-focus:text-main-orange peer-placeholder-shown:scale-100 text-main-orange"
    class:isLabelValid={value !== 0}
    class:font-medium={value !== null}
  >
    {label}
  </label>
  <select
    {id}
    class="field-select cursor-pointer ps-4 block py-2.5 w-full
                            md:text-xl bg-transparent border-gray-300"
    bind:value
    class:isValid={value !== 0}
    class:col-span-10={tooltip !== ""}
  >
    <slot></slot>
  </select>
  {#if tooltip}
    <div class="self-center text-center cursor-pointer" class:col-span-2={true}>
      <span use:tooltipElement title={tooltip} class="bi bi-info-circle"></span>
    </div>
  {/if}
</div>

<style>
  .isValid {
    border-color: green;
  }

  .isLabelValid {
    color: green;
  }

  .field-select {
    display: flex;
    align-items: center;
    background-color: #fff;
    border-radius: var(--border-radius);
    height: 60px;
    box-shadow: 0 4px 8px rgba(172, 186, 200, 0.1);
  }
  select:focus {
    border-color: var(--color-theme-2);
  }
</style>
