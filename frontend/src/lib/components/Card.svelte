<script>
  export let image,
    alt = "";
</script>

<div
  class="card-hover max-w-sm rounded-lg overflow-hidden bg-white border-4 border-transparent cursor-pointer"
  on:click
>
  <div class="px-6 py-4 align-center">
    <img class="mx-auto" height="60px" src={image} {alt} />
    {#if $$slots.description}
      <div class="description md:font-bold mb-2 md:text-lg mt-4">
        <slot name="description"></slot>
      </div>
    {/if}
  </div>
</div>

<style>
  .card-hover {
    position: relative;
    transform: translate3d(0px, 0%, 0px);
    background: #f5f5f6;
  }

  .card-hover:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--color-theme-2-light);
    border-radius: 50% 50% 0 0;
    transform: translateY(100%) scaleY(0.5);
    transition: all 0.6s ease;
  }

  .card-hover:after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 0;
    transform: translateY(0) scaleY(1);
    transition: all 0.4s ease;
  }

  .card-hover div {
    position: relative;
    width: 100%;
    overflow: hidden;
  }

  .card-hover:hover {
    transition: background 0.2s linear;
    transition-delay: 0.4s;
    border-color: var(--color-theme-2);
  }

  .card-hover:hover:after {
    border-radius: 0 0 50% 50%;
    transform: translateY(-100%) scaleY(0.5);
    transition-delay: 0;
  }

  .card-hover:hover:before {
    border-radius: 0;
    transform: translateY(0) scaleY(1);
    transition-delay: 0;
  }
</style>
