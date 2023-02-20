<script>
    import { page } from '$app/stores';
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let currentPage = '/game/lobby';
    
    onMount(() => {
        goto(currentPage)
    })
</script>