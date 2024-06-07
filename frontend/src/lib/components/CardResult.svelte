<script>
    export let image, alt = '', name = '', flying=false
</script>
<div class="rounded-lg overflow-hidden shadow-lg bg-white border-4 border-transparent cursor-pointer mb-5"
     on:click class:flying_card={flying}>
    <div class=" grid md:grid-cols-5 px-6 py-4 align-center">
        <div>
            <div class="flex h-100 border-2 border-main-orange rounded-md py-4 ">
                <img class="mx-auto max-h-20 self-center" src={image} alt={alt}>
            </div>
            <span class="font-bold max-sm:invisible">{name}</span>
        </div>
        {#if $$slots.description}
            <div class="mb-2 text-lg mt-4 md:col-span-4 self-center">
                    <slot name="description">
                    </slot>

            </div>
        {/if}
    </div>
</div>
<style>
     @media (min-width: 480px) {
        .flying_card {
            animation: animate 0.7s ease forwards;
        }

    }

    @keyframes animate {
        0% {
            transform: translateY(50%);
        }
        100% {
            transform: translateY(0%);
        }
    }
</style>
