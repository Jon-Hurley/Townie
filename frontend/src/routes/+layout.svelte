<script>
	import '../app.css';
    import { goto } from '$app/navigation'
	import { onMount } from 'svelte';
    import Navbar from './navbar.svelte';
    import AccountBar from './account-bar.svelte';
</script>

<AccountBar/>

<div class="m-0 w-full p-4">
    <slot/>
</div>

<Navbar/>