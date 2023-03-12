<script>
    import { goto } from '$app/navigation';
	import { Game } from '../../stores';
    import { page } from '$app/stores';
    import { browser } from '$app/environment'; 
    
    let gameStore = Game.store;

    $: if (browser) {
        console.log("RUNNING")
        const currPage = $page.path;
        const targetPage = '/game/' + ($gameStore?.game?.page || 'join');
        if (currPage !== targetPage) {
            goto(targetPage);
        }
    }
</script>

<slot/>