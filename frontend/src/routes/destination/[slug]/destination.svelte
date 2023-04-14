<script>
	import { acceptFriend, rejectFriend, sendFriendRequest } from '../../../requests/friend';
	import { userStore } from '../../../stores';
	import { pushPopup } from '../../../stores';
	import { goto } from '$app/navigation';
	import {
		buttonStyle,
		redStyle,
		greenStyle,
		blueStyle,
		indigoStyle,
		listItem
	} from '../../../css';
	import { submitDestRating } from '../../../requests/search';
	import { onMount } from 'svelte';
	const title = 'text-gray-700 font-semibold text-lg mt-6';
	const hr = 'my-1 bg-gray-100 h-[2px]';

	export let destination;

	onMount(async () => {
		console.log(destination);
		_setRating();
	});

	const _setRating = async () => {
		let stars = '';
		for (let i = 1; i <= 5; i++) {
			if (i <= destination.rating) {
				stars += '<span class="fa fa-star" style="color:orange"></span>';
			} else {
				stars += '<span class="fa fa-star"></span>';
			}
		}
		stars += ` (${destination.numRatings})`;
		document.getElementById('star-rating').innerHTML = stars;
	};

	const _submitRating = async (userRating) => {
		if (
			userRating == undefined ||
			userRating == null ||
			userRating == NaN ||
			userRating == '' ||
			userRating == ' ' ||
			userRating > 5 ||
			userRating < 0
		) {
			pushPopup(0, 'Please select a valid rating to submit.');
			return;
		}
		userRating = parseInt(userRating);
		console.log(userRating + ' ' + destination.rating + ' ' + destination.numRatings);
		let newRating =
			(destination.rating * destination.numRatings + userRating) / (destination.numRatings + 1);
		newRating = Math.round(newRating * 100) / 100;
		let newNumRatings = destination.numRatings + 1;
		pushPopup(
			1,
			'Rating submitted: ' +
				userRating +
				'(new rating: ' +
				newRating +
				')' +
				'(new num ratings: ' +
				newNumRatings +
				')'
		);
		await submitDestRating(destination._key, newRating, newNumRatings);
		destination.rating = newRating;
		destination.numRatings = newNumRatings;
		_setRating();
	};

	let media = [
		{
			name: 'Twitter',
			icon: 'M42,12.429c-1.323,0.586-2.746,0.977-4.247,1.162c1.526-0.906,2.7-2.351,3.251-4.058c-1.428,0.837-3.01,1.452-4.693,1.776C34.967,9.884,33.05,9,30.926,9c-4.08,0-7.387,3.278-7.387,7.32c0,0.572,0.067,1.129,0.193,1.67c-6.138-0.308-11.582-3.226-15.224-7.654c-0.64,1.082-1,2.349-1,3.686c0,2.541,1.301,4.778,3.285,6.096c-1.211-0.037-2.351-0.374-3.349-0.914c0,0.022,0,0.055,0,0.086c0,3.551,2.547,6.508,5.923,7.181c-0.617,0.169-1.269,0.263-1.941,0.263c-0.477,0-0.942-0.054-1.392-0.135c0.94,2.902,3.667,5.023,6.898,5.086c-2.528,1.96-5.712,3.134-9.174,3.134c-0.598,0-1.183-0.034-1.761-0.104C9.268,36.786,13.152,38,17.321,38c13.585,0,21.017-11.156,21.017-20.834c0-0.317-0.01-0.633-0.025-0.945C39.763,15.197,41.013,13.905,42,12.429',
			link:
				'https://twitter.com/intent/tweet?text=Check%20out%20this%20Townie%20Destination%20I%20played%3A%0A' +
				window.location.href
		},
		{
			name: 'Reddit',
			icon: 'M12.193 19.555c-1.94-1.741-4.79-1.727-6.365.029-1.576 1.756-1.301 5.023.926 6.632L12.193 19.555zM35.807 19.555c1.939-1.741 4.789-1.727 6.365.029 1.575 1.756 1.302 5.023-.927 6.632L35.807 19.555zM38.32 6.975A3.5 3.5 0 1 0 38.32 13.975 3.5 3.5 0 1 0 38.32 6.975z',
			link:
				'https://www.reddit.com/submit?&title=Check%20out%20this%20Townie%20Destination%20I%20played%3A%0A&url=' +
				window.location.href
		},
		{
			name: 'Mail',
			icon: 'M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75',
			link:
				'mailto:?&body=Check%20out%20this%20Townie%20Destination%20I%20played%3A%0Alink' +
				window.location.href
		},
		{
			name: 'Whatsapp',
			icon: 'M4.868,43.303l2.694-9.835C5.9,30.59,5.026,27.324,5.027,23.979C5.032,13.514,13.548,5,24.014,5c5.079,0.002,9.845,1.979,13.43,5.566c3.584,3.588,5.558,8.356,5.556,13.428c-0.004,10.465-8.522,18.98-18.986,18.98c-0.001,0,0,0,0,0h-0.008c-3.177-0.001-6.3-0.798-9.073-2.311L4.868,43.303z',
			link:
				'https://api.whatsapp.com/send/?text=Check%20out%20this%20Townie%20Destination%20I%20played%3A%0A' +
				window.location.href +
				'&type=custom_url'
		},
		{
			name: 'Copy Link',
			icon: 'M4.868,43.303l2.694-9.835C5.9,30.59,5.026,27.324,5.027,23.979C5.032,13.514,13.548,5,24.014,5c5.079,0.002,9.845,1.979,13.43,5.566c3.584,3.588,5.558,8.356,5.556,13.428c-0.004,10.465-8.522,18.98-18.986,18.98c-0.001,0,0,0,0,0h-0.008c-3.177-0.001-6.3-0.798-9.073-2.311L4.868,43.303z',
			link: '' + window.location.href
		}
	];

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

<link
	rel="stylesheet"
	href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
/>

<div class="my-5 w-full">
	<div class="text-gray-700 font-bold text-3xl text-center">
		Destination: {destination.name}
	</div>
	<!-- <div class="text-gray-700 text-md text-center">
		{new Date(summary.game.startTime).toLocaleString()}
	</div> -->
</div>

<div class={title}>Share Destination!</div>
<hr class={hr} />

<div class="flex flex-row justify-center">
	{#each media as media}
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			style="display: flex; justify-content: center;"
			class="
			border-gray-400 border-2 rounded-full
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
					navigator.clipboard.writeText('' + window.location.href);
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
<hr class={hr} style="margin-top:10px;" />

<div class={title} style="margin-bottom:10px;">
	Theme: <div class={indigoStyle} style="display:inline-block">
		{destination.theme}
	</div>
	<div
		id="star-rating"
		class="fa-pull-right {buttonStyle}"
		style="display:inline-block;text-align:right;"
	/>
	<hr class={hr} />
</div>

<form>
	<label for="userRatingField">Rating:</label>
	<button
		class="{buttonStyle}{redStyle}"
		style="padding: 5px;"
		onclick="this.parentNode.querySelector('#userRatingField').stepDown()">-</button
	>
	<input
		type="number"
		placeholder="0-5"
		style="border:2px;color:indigo;border-color:indigo;border-radius:5px;padding:5px;width:40px;text-align:center;"
		id="userRatingField"
		name="userRatingField"
		min="0.0"
		max="5.0"
		step="0.1"
		value="0.0"
	/>
	<button
		class="{buttonStyle}{greenStyle}"
		style="padding: 5px;"
		onclick="this.parentNode.querySelector('#userRatingField').stepUp()">+</button
	>
	<button
		type="submit"
		class="{buttonStyle}{indigoStyle}"
		style="float: right;"
		on:click={() => {
			let temp = document.getElementById('userRatingField').value;
			_submitRating(temp);
		}}>Submit</button
	>
</form>

<div class={title}>Tips</div>
<hr class={hr} />
<div class="h-full">
	<div class="flex flex-wrap justify-center gap-2 px-2 py-4">
		{#if !destination.tips.length}
			<div>No destinations to display.</div>
		{/if}
		<ul>
			{#each destination.tips as t}
				<li class={buttonStyle} style="display:block;margin:5px">{t}</li>
				<!-- <div
				
                "
			>
				Points: {t.points}
				{t.name}
			</div> -->
			{/each}
		</ul>
	</div>
</div>

<button class="{buttonStyle}{indigoStyle}" onclick="window.close()">Return To Game</button>
