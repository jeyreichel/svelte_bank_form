<script>
  export let inversed = false,
    color = "main-orange",
    class_name = "";
</script>

{#if inversed}
  <button
    on:click
    class="bg-transparent hover:bg-main-orange max-sm:flex max-sm:flex-wrap
        text-main-black font-semibold hover:text-main-black py-2 px-4 border
        border-{color} hover:border-transparent rounded-md {class_name}"
  >
    <slot></slot>
  </button>
{:else}
  <button
    on:click
    class="hover:bg-transparent bg-main-orange max-sm:flex max-sm:flex-nowrap
        hover:text-main-black font-semibold text-main-black py-2 px-4 border
        hover:border-main-orange border-transparent rounded-md {class_name}"
  >
    <slot></slot>
  </button>
{/if}
