<script>
	import '../app.css';
    import Navbar from './navbar.svelte';
    import AccountBar from './account-bar.svelte';
</script>

<AccountBar/>

<div class="m-0 w-full p-4">
    <slot/>
</div>

<Navbar/>