<script>
  // @ts-nocheck

  import { tooltipElement } from "$lib/jscomponent/tooltip.js";

  export let id,
    type,
    value = type === "number" ? null : "",
    tooltip = "",
    valid,
    dont_accept_figures = false,
    dont_accept_string = false,
    dont_accept_space = false;
  let isFocused;
  const onFocus = () => {
    isFocused = true;
  };
  const onBlur = () => {
    isFocused = false;
  };

  const handleKeyDown = (event) => {
    // Allow only number keys (0-9) and certain control keys (e.g., backspace, delete, arrow keys)
    const keyCode = event.keyCode || event.which;
    const allowedKeys = [8, 9, 37, 39, 46]; // Add more keycodes as needed
    if ((keyCode < 48 || keyCode > 57) && !allowedKeys.includes(keyCode)) {
      event.preventDefault();
    }
  };

  const handleSpaceDown = (event) => {
    const keyCode = event.keyCode || event.which;
    const allowedKeys = [8, 9, 37, 39, 46, 110, 188, 190]; // Add more keycodes as needed
    if ((keyCode < 48 || keyCode > 57) && !allowedKeys.includes(keyCode)) {
      event.preventDefault();
    }
  };
</script>

<div class:grid={tooltip !== ""} class:grid-cols-12={tooltip !== ""}>
  <div
    class="relative z-0 w-full group self-center"
    class:col-span-10={tooltip !== ""}
  >
    {#if type === "number"}
      <input
        type="number"
        {id}
        bind:value
        class="block w-full md:text-xl text-gray-500 bg-transparent
                                border-gray-300 appearance-none focus:outline-none
                               focus:ring-0 peer"
        on:input
        class:isValid={value !== null && valid === undefined}
        class:border-red-600={value !== null && valid !== undefined}
        class:text-red-600={value !== null && valid !== undefined}
        class:border-green={valid === undefined}
        on:focus={onFocus}
        on:blur={onBlur}
        placeholder=" "
        {...$$props}
      />
      <label
        for={id}
        class="peer-focus:font-medium absolute md:text-xl text-gray-500 duration-300
                               transform -translate-y-10 translate-x-4 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0
                               peer-focus:text-main-orange peer-placeholder-shown:scale-100
                               peer-placeholder-shown:translate-y-1
                               peer-focus:scale-75 peer-focus:-translate-y-10"
        class:isLabelValid={value !== null && valid === undefined}
        class:text-red-600={value !== null && valid !== undefined}
        class:font-medium={value !== null && valid !== undefined}
      >
        <slot name="label"></slot>
      </label>
      {#if $$slots.suffix}
        <span class="pxSpan text-gray-500"><slot name="suffix"></slot></span>
      {/if}
    {:else}
      {#if dont_accept_figures}
        <input
          type="text"
          {id}
          bind:value
          class="block w-full md:text-xl text-gray-500 bg-transparent border
                                border-gray-300 appearance-none focus:outline-none
                               focus:ring-0 peer"
          on:input
          class:isValid={value !== "" && valid === undefined}
          class:text-red-600={value !== "" && valid !== undefined}
          class:border-red-600={value !== "" && valid !== undefined}
          on:focus={onFocus}
          on:blur={onBlur}
          placeholder=" "
          {...$$props}
          onkeydown="return /[a-zA-Z\u00C0-\u017F -]/i.test(event.key)"
        />
      {:else if dont_accept_string}
        <input
          type="text"
          {id}
          bind:value
          class="block w-full md:text-xl text-gray-500 bg-transparent border
                                border-gray-300 appearance-none focus:outline-none
                               focus:ring-0 peer"
          on:input
          class:isValid={value !== "" && valid === undefined}
          class:border-red-600={value !== "" && valid !== undefined}
          class:text-red-600={value !== "" && valid !== undefined}
          on:focus={onFocus}
          on:blur={onBlur}
          placeholder=" "
          {...$$props}
          on:keydown={handleKeyDown}
        />
      {:else if dont_accept_space}
        <input
          type="text"
          {id}
          bind:value
          class="block w-full md:text-xl text-gray-500 bg-transparent border
                                border-gray-300 appearance-none focus:outline-none
                               focus:ring-0 peer"
          on:input
          class:isValid={value !== "" && valid === undefined}
          class:border-red-600={value !== "" && valid !== undefined}
          class:text-red-600={value !== "" && valid !== undefined}
          on:focus={onFocus}
          on:blur={onBlur}
          placeholder=" "
          {...$$props}
          on:keydown={handleSpaceDown}
        />
      {:else}
        <input
          type="text"
          {id}
          bind:value
          class="block w-full md:text-xl text-gray-500 bg-transparent border
                                border-gray-300 appearance-none focus:outline-none
                               focus:ring-0 peer"
          on:input
          class:isValid={value !== "" && valid === undefined}
          class:border-red-600={value !== "" && valid !== undefined}
          on:focus={onFocus}
          on:blur={onBlur}
          placeholder=" "
          {...$$props}
        />
      {/if}
      <label
        for={id}
        class="peer-focus:font-medium absolute md:text-xl text-gray-500 duration-300
                               transform -translate-y-10 translate-x-4 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0
                               peer-focus:text-main-orange peer-placeholder-shown:scale-100
                               peer-placeholder-shown:translate-y-1
                               peer-focus:scale-75 peer-focus:-translate-y-10"
        class:isLabelValid={value !== "" && valid === undefined}
        class:text-red-600={value !== "" && valid !== undefined}
        class:font-medium={value !== "" && valid !== undefined}
      >
        <slot name="label"></slot>
      </label>
    {/if}
  </div>
  {#if tooltip}
    <div class="self-center text-center cursor-pointer" class:col-span-2={true}>
      <span use:tooltipElement title={tooltip} class="bi bi-info-circle"></span>
    </div>
  {/if}
  {#if value !== null && value !== "" && valid !== undefined && valid.type !== "type" && !isFocused}
    <span class:text-red-600={true} class:col-span-12={true}>
      {valid["message"]}
    </span>
  {/if}
</div>

<style>
  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin-right: 10%;
  }

  input {
    display: flex;
    align-items: center;
    border-radius: var(--border-radius);
    height: 60px;
    box-shadow: 0 4px 8px rgba(172, 186, 200, 0.1);
  }

  input:focus {
    border-color: var(--color-theme-2);
  }

  .isValid {
    border-color: green;
  }

  .isLabelValid {
    color: green;
    font-weight: 500;
  }

  .pxSpan {
    position: absolute;
    top: 19px;
    right: 10px;
  }
</style>
