<script>
	import '../app.css';
    import { goto } from '$app/navigation'
	import { onMount } from 'svelte';
    import Navbar from './navbar.svelte';
</script>

<slot />

<Navbar/>