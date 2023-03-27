<script>
    import { goto } from '$app/navigation';
	import { Game } from '../../classes/Game';
    import { page } from '$app/stores';
    import { browser } from '$app/environment'; 
	import Modal from '../../general-components/modal.svelte';
    
    let gameStore = Game.store;
    let gameMessageObj = Game.messageObj;
    console.log({gameMessageObj})

    $: if (browser) {
        console.log("RUNNING")
        const currPage = $page.path;
        const targetPage = '/game/' + ($gameStore?.game?.page || 'join');
        if (currPage !== targetPage) {
            goto(targetPage);
        }
    }
</script>

<Modal
	{...$gameMessageObj}
/>

<slot/>