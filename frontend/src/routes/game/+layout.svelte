<script>
    import { goto } from '$app/navigation';
	import { gameStore, userStore } from '../../stores';
    
    $: {
        if ($userStore)
            goto(`/game/${$gameStore?.game?.page || 'join'}`)
    };
</script>

<slot/>