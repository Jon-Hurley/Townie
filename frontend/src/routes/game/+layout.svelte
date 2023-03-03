<script>
	import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
	import { gameStore } from '../../stores';
    import { page } from '$app/stores';
    
    $: if ($gameStore) {
        console.log("UPDATING PAGE")

        const currPage = $page.path;
        const targetPage = `/game/${$gameStore?.game?.page || 'join'}/`;
        if (currPage !== targetPage) {
            console.log("Going to: ", targetPage)
            goto(targetPage);
        }
        console.log($gameStore);
    }
</script>

<slot/>