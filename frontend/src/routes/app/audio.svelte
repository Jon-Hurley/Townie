<script>
    import { primaryAudio } from '../../stores';
    import Kahoot from '$lib/lobby-classic-game.mp3';
    import Moonshine from '$lib/moonshine.mp3';
    import ThemeSong from '$lib/theme-song.mp3';
	import { onDestroy } from 'svelte';

    let audioElement;

    $: if ($primaryAudio) {
        if (audioElement) {
            audioElement.pause();
            audioElement.src = (
                $primaryAudio === 'Kahoot' ? Kahoot
                : $primaryAudio === 'Moonshine' ? Moonshine
                : $primaryAudio === 'Townie Theme' ? ThemeSong
                : ''
            );
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

<audio
    bind:this={audioElement}
    loop="true"
    autostart="true"
    style="height: 0px; width: 0px;"
/>