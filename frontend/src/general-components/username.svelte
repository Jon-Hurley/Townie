<script>
	import { userStore } from "../stores";
    export let user = $userStore, boldness = 'semibold';
</script>

{#if user.isPremium}
    <div class="shimmer text-amber-400 font-{boldness}">
        {user.username}
    </div>
{:else}
    <div>
        {user.username}
    </div>
{/if}