<script>
	import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
	import { gamePage, unsubscribeToLocation } from '../../stores';
    
    onMount(() => {
        goto($gamePage);
    });
</script>

<slot/>