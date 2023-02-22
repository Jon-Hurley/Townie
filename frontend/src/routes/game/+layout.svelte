<script>
	import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
	import { gamePage, groupStore } from '../../stores';
    
    onMount(() => {
        gamePage.subscribe(p => {
            console.log("going to page...", p)
            goto(p);
        });
    });

    groupStore.subscribe(groupData => {
        console.log({groupData});
    });

    // onDestroy(() => {
    //     if (sub) {
    //         unsubscribeToLocation
    //     }
    // });
</script>

<slot/>