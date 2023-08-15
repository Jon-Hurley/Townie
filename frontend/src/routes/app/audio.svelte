<script>
	import { primaryAudio } from '../../stores';
	import { onDestroy } from 'svelte';

	let audioElement;

	$: if ($primaryAudio) {
		if (audioElement) {
			audioElement.pause();
			audioElement.src =
				$primaryAudio === 'Kahoot'
					? '/audio/lobby-classic-game.mp3'
					: $primaryAudio === 'Moonshine'
					? '/audio/moonshine.mp3'
					: $primaryAudio === 'Townie Theme'
					? '/audio/theme-song.mp3'
					: $primaryAudio === 'Hound Dog'
					? '/audio/hound-dog.mp3'
					: $primaryAudio === 'Munch'
					? '/audio/munch.mp3'
					: $primaryAudio === 'Flacko'
					? '/audio/flacko.mp3'
					: '';
			audioElement.play();
		}
	} else {
		audioElement?.pause();
	}

	onDestroy(() => {
		audioElement?.pause();
	});
</script>

<audio
	bind:this={audioElement}
	loop="true"
	autostart="true"
	style="height: 0px; width: 0px;"
/>