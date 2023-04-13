<script>
	import { slide, fade } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';

	import Join from '$lib/assets/Tutorial-join.jpg';
	import Settings1 from '$lib/assets/Tutorial-Settings-1.jpg';
	import Settings2 from '$lib/assets/Tutorial-Settings-2.jpg';
	import Settings3 from '$lib/assets/Tutorial-Settings-3.jpg';
	import Settings4 from '$lib/assets/Tutorial-Settings-4.jpg';
	import Settings5 from '$lib/assets/Tutorial-Settings-5.jpg';
	import Map from '$lib/assets/Tutorial-Map.jpg';

	const images = [
		{
			src: Join,
			description: 'Join-1'
		},
		{
			src: Settings1,
			description: 'Settings-1'
		},
		{
			src: Settings2,
			description: 'Settings-2'
		},
		{
			src: Settings3,
			description: 'Settings-3'
		},
		{
			src: Settings4,
			description: 'Settings-4'
		},
		{
			src: Settings5,
			description: 'Settings-5'
		},
		{
			src: Map,
			description: 'Map-1'
		}
	];

	let currentSlideItem = 0;
	
  const nextImage = () => {
		currentSlideItem = (currentSlideItem + 1) % images.length;
	};
	
  const prevImage = () => {
    currentSlideItem = (currentSlideItem + images.length - 1) % images.length;
	};
</script>

{#each [images[currentSlideItem]] as item (currentSlideItem)}
  <img
    in:slide
    src={item.src}
    alt={item.description}
    style="max-height: calc(100vh - 120px - 4rem); margin: auto;"
  />
{/each}

<div class="carousel-buttons">
  <!-- Previous Button -->
  <button
    class="absolute bottom-[5rem] left-4 md:left-40  lg:left-96 z-10
      bg-gray-800 rounded-full
      px-1 py-1
      opacity-50 text-gray-400"
    on:click={() => prevImage()}
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="w-6 h-6"
    >
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
    </svg>
  </button>

  <!-- Next Button -->
  <button
    class="absolute bottom-[5rem] right-4 md:right-40 lg:right-96 z-10
      bg-gray-800 rounded-full
      px-1 py-1
      opacity-50 text-gray-400"
    on:click={() => nextImage()}
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="w-6 h-6"
    >
      <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
    </svg>
  </button>
</div>
