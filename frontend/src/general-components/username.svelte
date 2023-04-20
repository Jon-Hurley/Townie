<script>
	import { userStore } from "../stores";
    export let user = null, boldness = 'semibold';

    $: realUser = user || $userStore;
</script>

{#if realUser.isPremium}
    <div class="shimmer text-amber-400 font-{boldness}">
        {realUser.username}
    </div>
{:else}
    <div>
        {realUser.username}
    </div>
{/if}