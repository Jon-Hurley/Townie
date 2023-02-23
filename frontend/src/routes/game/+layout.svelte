<script>
	import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
	import { gamePage, gameStore } from '../../stores';
    
    onMount(() => {
        gamePage.subscribe(p => {
            console.log("going to page...", p)
            goto(p);
        });
        gameStore.subscribe(gameData => {
            console.log({gameData});
        });
    });

    // onDestroy(() => {
    //     if (sub) {
    //         unsubscribeToLocation
    //     }
    // });
</script>

<slot/>