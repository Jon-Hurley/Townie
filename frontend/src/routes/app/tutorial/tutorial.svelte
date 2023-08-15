<script>
	import { slide } from 'svelte/transition';
	import { hr, largeTitle } from '../../../css';

	const images = [
		{
			src: '/images/Join.jpg',
			description: 'Join or create a game'
		},
		{
			src: '/images/Settings-1.jpg',
			description: 'Settings-1'
		},
		{
			src: '/images/Settings-2.jpg',
			description: 'Settings-2'
		},
		{
			src: '/images/Settings-3.jpg',
			description: 'Settings-3'
		},
		{
			src: '/images/Settings-4.jpg',
			description: 'Settings-4'
		},
		{
			src: '/images/Settings-5.jpg',
			description: 'Settings-5'
		},
    {
			src: '/images/Settings-6.jpg',
			description: 'Settings-6'
		},
    {
			src: '/images/Settings-7.jpg',
			description: 'Settings-7'
		},
		{
			src: '/images/Map.jpg',
			description: 'Map-1'
		},
		{
			src: '/images/inGame.jpg',
			description: 'In-Game-Options'
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

<div class="{largeTitle}">
  Tutorial
</div>
<hr class="{hr}"/>

{#each [images[currentSlideItem]] as item (currentSlideItem)}
  <img
    in:slide
    src={item.src}
    alt={item.description}
    style="max-height: calc(100vh - 220px - 4rem); margin: auto;"
  />
{/each}

<div class="carousel-buttons">
  <!-- Previous Button -->
  <button
    class="
      absolute bottom-[5rem] left-4 md:left-40 lg:left-96 z-10
      bg-gray-800 rounded-full
      px-1 py-1
      opacity-50 text-gray-400
    "
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
