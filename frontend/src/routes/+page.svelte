<script>
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { userStore } from '../stores';
	import { onMount } from 'svelte';
  
    onMount(() => {
        if ($userStore) {
            goto('/login');
        } else {
            goto('/login')
        }
    });
</script>