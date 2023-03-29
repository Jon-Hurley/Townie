<script>
    import {slide, fade} from 'svelte/transition'; 
    import {elasticInOut} from 'svelte/easing';

    let tutorial = false;

    const images = [
      {
        src: "/Tutorial-Settings-1",
        description: "Settings-1",
      },
      {
        src: "%sveltekit.assets%/Tutorial-Settings-2",
        description: "Settings-2",
      },
      {
        src: "%sveltekit.assets%/Tutorial-Settings-3",
        description: "Settings-3",
      },
      {
        src: "%sveltekit.assets%/Tutorial-Settings-4",
        description: "Settings-4",
      },
      {
        src: "%sveltekit.assets%/Tutorial-Settings-5",
        description: "Setings-5",
      },
      {
        src: "/Tutorial-Map",
        description: "Map-1",
      },
    ];

    let currentSlideItem = 0;
    const nextImage = () => {
        currentSlideItem = (currentSlideItem + 1) % images.length;
    }
    const prevImage = () => {
        if (currentSlideItem != 0) {
            currentSlideItem = (currentSlideItem - 1) % images.length;
        } else {
            currentSlideItem = images.length - 1;
        }
    }
</script>
  
{#if tutorial}
      {#each [images[currentSlideItem]] as item (currentSlideItem)}
        <img in:slide="{{ duration: 1000, easing: elasticInOut}}" out:fade src={item.url} alt={item.description} height="full"/>
      {/each}
      <div class="carousel-buttons">
        <!-- Previous Button -->
        <button class="absolute bottom-[5rem] left-4 z-10
            bg-gray-800 rounded-full
            px-1 py-1
            opacity-50 text-gray-400"
            on:click={() => prevImage()}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>                     
        </button> 

        <!-- Next Button -->
        <button class="absolute bottom-[5rem] right-4 z-10
            bg-gray-800 rounded-full
            px-1 py-1
            opacity-50 text-gray-400"
            on:click={() => nextImage()}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>                     
        </button> 

        <!-- Close Button -->
        <button class="absolute top-[5rem] right-4 z-10
            bg-red-100 rounded-full
            opacity-80 text-red-600"
            on:click={() => tutorial = false}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>               
        </button> 
      </div>

{:else}
    <button class="absolute bottom-[5rem] right-4 z-10
        bg-gray-800 rounded-full
        px-1 py-1
        opacity-50 text-gray-400"
        on:click={() => {
            tutorial = true;
            console.log(tutorial);
        }}>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
        </svg>        
    </button> 
{/if}