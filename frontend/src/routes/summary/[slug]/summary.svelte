<script>
	import { acceptFriend, rejectFriend, sendFriendRequest } from '../../../requests/friend';
	import { userStore } from '../../../stores';
	import { buttonStyle, redStyle, greenStyle, blueStyle, indigoStyle } from '../../../css';
	import Modal from '../../../components/modal.svelte';
	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-2 bg-gray-100 h-[2px]';

	export let summary;

	let messageObj = {
		status: 0,
		message: null,
		dest: null
	};
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

<Modal {...messageObj} />

<div class="my-5 w-full">
	<div class="text-gray-700 font-bold text-3xl text-center">
		{summary.gameID}
	</div>
	<div class="text-gray-700 text-md text-center">
		#{summary.key}
	</div>
</div>

<div class={title}>Share Game!</div>
<hr class={hr} />
<div class="h-full overflow-auto">
	<div class="flex flex-wrap justify-center gap-2 px-2 py-4">
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
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d={p.rating} />
			</svg>

			Twitter
		</div>

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
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d={p.rating} />
			</svg>

			Facebook
		</div>

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
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d={p.rating} />
			</svg>

			LinkedIn
		</div>
	</div>
</div>

<div class={title}>Start Time:</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	{summary.startTime}
</div>

<div class={title}>How many finished?</div>
<hr class={hr} />
<div class="px-2 py-4 uppercase">
	{summary.numFinished}/{summary.members.length}
</div>

<div class={title}>Destinations</div>
<hr class={hr} />
<div class="h-full overflow-auto">
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
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d={p.rating} />
				</svg>

				{p.name}
			</div>
		{/each}
	</div>
</div>

<div class={title}>Participants</div>
<hr class={hr} />
<div class="h-full overflow-auto">
	<div class="flex flex-wrap justify-center gap-2 px-2 py-4">
		{#if !summary.members.length}
			<div>No participants to display.</div>
		{/if}
		{#each summary.members as r}
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
