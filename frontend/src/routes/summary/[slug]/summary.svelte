<script>
	import { onMount } from 'svelte';
	import { pushPopup } from '../../../stores';
	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-2 bg-gray-100 h-[2px]';

	export let summary;
	onMount(async () => {
		console.log(summary);
	});

	let media = [
		{
			name: 'Twitter',
			icon: 'M42,12.429c-1.323,0.586-2.746,0.977-4.247,1.162c1.526-0.906,2.7-2.351,3.251-4.058c-1.428,0.837-3.01,1.452-4.693,1.776C34.967,9.884,33.05,9,30.926,9c-4.08,0-7.387,3.278-7.387,7.32c0,0.572,0.067,1.129,0.193,1.67c-6.138-0.308-11.582-3.226-15.224-7.654c-0.64,1.082-1,2.349-1,3.686c0,2.541,1.301,4.778,3.285,6.096c-1.211-0.037-2.351-0.374-3.349-0.914c0,0.022,0,0.055,0,0.086c0,3.551,2.547,6.508,5.923,7.181c-0.617,0.169-1.269,0.263-1.941,0.263c-0.477,0-0.942-0.054-1.392-0.135c0.94,2.902,3.667,5.023,6.898,5.086c-2.528,1.96-5.712,3.134-9.174,3.134c-0.598,0-1.183-0.034-1.761-0.104C9.268,36.786,13.152,38,17.321,38c13.585,0,21.017-11.156,21.017-20.834c0-0.317-0.01-0.633-0.025-0.945C39.763,15.197,41.013,13.905,42,12.429',
			link: 'https://twitter.com/intent/tweet?text=Check%20out%20this%20Townie%20game%20I%20played%3A%0Alink'
		},
		{
			name: 'Reddit',
			icon: 'M12.193 19.555c-1.94-1.741-4.79-1.727-6.365.029-1.576 1.756-1.301 5.023.926 6.632L12.193 19.555zM35.807 19.555c1.939-1.741 4.789-1.727 6.365.029 1.575 1.756 1.302 5.023-.927 6.632L35.807 19.555zM38.32 6.975A3.5 3.5 0 1 0 38.32 13.975 3.5 3.5 0 1 0 38.32 6.975z',
			link: 'https://www.reddit.com/submit?&title=Check%20out%20this%20Townie%20game%20I%20played%3A%0A&url=townie.com'
		},
		{
			name: 'Mail',
			icon: 'M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75',
			link: 'mailto:?&body=Check%20out%20this%20Townie%20game%20I%20played%3A%0Alink'
		},
		{
			name: 'Whatsapp',
			icon: 'M4.868,43.303l2.694-9.835C5.9,30.59,5.026,27.324,5.027,23.979C5.032,13.514,13.548,5,24.014,5c5.079,0.002,9.845,1.979,13.43,5.566c3.584,3.588,5.558,8.356,5.556,13.428c-0.004,10.465-8.522,18.98-18.986,18.98c-0.001,0,0,0,0,0h-0.008c-3.177-0.001-6.3-0.798-9.073-2.311L4.868,43.303z',
			link: 'https://api.whatsapp.com/send/?text=Check%20out%20this%20Townie%20game%20I%20played%3A%0Alink&type=custom_url'
		},
		{
			name: 'Copy Link',
			icon: 'M4.868,43.303l2.694-9.835C5.9,30.59,5.026,27.324,5.027,23.979C5.032,13.514,13.548,5,24.014,5c5.079,0.002,9.845,1.979,13.43,5.566c3.584,3.588,5.558,8.356,5.556,13.428c-0.004,10.465-8.522,18.98-18.986,18.98c-0.001,0,0,0,0,0h-0.008c-3.177-0.001-6.3-0.798-9.073-2.311L4.868,43.303z',
			link: 'link'
		}
	];

	function amperoctoplus(s) {
		s = s.replace(/&/g, '%26');
		s = s.replace(/#/g, '%23');
		s = s.replace(/\+/g, '%2B');
		s = s.replace(/@/g, '%40');
		s = s.replace(/:/g, '%3A');
		return s;
	}

	/*
        Twitter: 
        https://twitter.com/intent/tweet?text=Check%20out%20this%20Townie%20game%20I%20played%3A%0A + link
    
        Whatsapp: 
        https://api.whatsapp.com/send/?text=Check%20out%20this%20Townie%20game%20I%20played%3A%0A + link + &type=custom_url
    
        Mail:
        mailto:?&body=Check%20out%20this%20Townie%20game%20I%20played%3A%0A + link

        Reddit:
        https://www.reddit.com/submit?&title=Check%20out%20this%20Townie%20game%20I%20played%3A%0A&url= + link

        Copy Link:
    */
</script>

<div class="my-5 w-full">
	<div class="text-gray-700 font-bold text-3xl text-center">
		{summary.game._id}
	</div>
	<div class="text-gray-700 text-md text-center">
		#{summary.game._key}
	</div>
</div>

<div class={title}>Share Game!</div>
<hr class={hr} />

<div class="flex flex-row justify-center">
	{#each media as media}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			class="
			border-gray-200 border-4 rounded-full
			p-3 m-0
			text-indigo-500 font-semibold
			w-24 h-24
			flex flex-col items-center justify-center
			text-xs
			hover:scale-110 duration-200
			z-100
			overflow-visible
			cursor-pointer
		"
			on:click={() => {
				if (media.name === 'Copy Link') {
					navigator.clipboard.writeText('link');
					pushPopup(1, 'Link copied to clipboard!');
				} else {
					window.open(media.link, '_blank');
				}
			}}
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 48 48"
				stroke-width="1.5"
				stroke="currentColor"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d={media.icon} />
			</svg>

			<div class="text-center">{media.name}</div>
		</div>
	{/each}
</div>

<div class={title}>Start Time:</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	{new Date(summary.game.startTime * 1000).toLocaleString()}
</div>

<div class={title}>How many finished?</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	{summary.game.numFinished}/{summary.players.length}
</div>

<div class={title}>Destinations</div>
<hr class={hr} />
<div class="h-full">
	<div class="flex flex-wrap justify-center gap-2 px-2 py-4">
		{#if !summary.destinations.length}
			<div>No destinations to display.</div>
		{/if}
		{#each summary.destinations as p}
			<div
				class="
                    border-gray-200 border-4 rounded-full
                    p-3 m-0
                    text-indigo-500 font-semibold
                    w-24 h-24
                    flex flex-col items-center justify-center
                    text-xs
                    hover:scale-110 duration-200
                    z-100
                    overflow-visible
                    cursor-pointer
                "
			>
				{p.rating}
				{p.name}
			</div>
		{/each}
	</div>
</div>

<div class={title}>Participants</div>
<hr class={hr} />
<div class="h-full">
	<div class="flex flex-wrap justify-center gap-2 px-2 py-4">
		{#if !summary.players.length}
			<div>No participants to display.</div>
		{/if}
		{#each summary.players as r}
			<li
				class="
                            w-full
                            text-gray-900
                            z-10
                            bg-white
                            relative
                            cursor-pointer
                            p-2
                            flex
                            justify-between
                        "
			>
				<a href={'/user/' + r.key}>
					<!-- <img></img> -->
					{r.username} #{r.key}
				</a>
			</li>
		{/each}
	</div>
</div>
