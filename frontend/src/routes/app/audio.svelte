<script>
	import { primaryAudio } from '../../stores';
	import Kahoot from '$lib/lobby-classic-game.mp3';
	import Moonshine from '$lib/moonshine.mp3';
	import ThemeSong from '$lib/theme-song.mp3';
	import HoundDog from '$lib/hound-dog.mp3';
	import Munch from '$lib/munch.mp3';
	import Flacko from '$lib/flacko.mp3';
	import { onDestroy } from 'svelte';

	let audioElement;

	$: if ($primaryAudio) {
		if (audioElement) {
			audioElement.pause();
			audioElement.src =
				$primaryAudio === 'Kahoot'
					? Kahoot
					: $primaryAudio === 'Moonshine'
					? Moonshine
					: $primaryAudio === 'Townie Theme'
					? ThemeSong
					: $primaryAudio === 'Hound Dog'
					? HoundDog
					: $primaryAudio === 'Munch'
					? Munch
					: $primaryAudio === 'Flacko'
					? Flacko
					: '';
			audioElement.play();
		}
	} else {
		if (audioElement) {
			audioElement.pause();
		}
	}

	onDestroy(() => {
		audioElement?.pause();
	});
</script>

<audio bind:this={audioElement} loop="true" autostart="true" style="height: 0px; width: 0px;" />
