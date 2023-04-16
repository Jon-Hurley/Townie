<script>
	import { gridContainer } from "../../../css";
	import Purchase from "../../../general-components/purchase.svelte";
	import { activatePurchase } from "../../../requests/store";
	import { userStore } from "../../../stores";

    const _activatePurchase = async (p) => {
        await activatePurchase(p._key)
    }
</script>

{#if $userStore?.purchases?.length}
    <div class="{gridContainer}">
        {#each $userStore?.purchases as p}
            <Purchase
                p={p}
                onClick={() => _activatePurchase(p)}
                isActive={p.isActive}
            />
        {/each}
    </div>
{:else}
    <div class="flex gap-2">
        <div>You have no purchases</div>
    </div>
{/if}