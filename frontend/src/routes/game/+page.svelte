<script>
	import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
	import { unsubscribeToLocation } from '../../stores';
</script>

<slot/>