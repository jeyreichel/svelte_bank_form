<script>
  import "./styles.css";
  import "flowbite/dist/flowbite.css";
</script>

<div class="app">
  <main>
    <slot />
  </main>
</div>

<style lang="postcss">
  .app {
    display: flex;
    flex-direction: column;
    min-height: 50vh;
  }

  main {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    width: 100%;
    max-width: 64rem;
    margin: 0 auto;
    box-sizing: border-box;
  }
</style>
