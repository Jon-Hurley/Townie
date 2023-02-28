<script>
	import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
	import { gameStore } from '../../stores';
    import { page } from '$app/stores';
    
    onMount(() => {
        gameStore.subscribe(gameData => {
            const currPage = $page.path;
            const targetPage = `/game/${gameData?.game?.page || 'join'}/`;
            if (currPage !== targetPage) {
                console.log("Going to: ", targetPage)
                goto(targetPage);
            }
            console.log(gameData);
        });
    });
</script>

<slot/>