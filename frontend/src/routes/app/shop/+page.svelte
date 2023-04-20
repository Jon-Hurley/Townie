<script>
	import { onMount } from "svelte";
	import { largeTitle, hr, gridContainer } from "../../../css";
    import { getPurchasables, makePurchase } from "../../../requests/store";
	import Loading from "../../../general-components/loading.svelte";
	import { pushPopup, userStore } from "../../../stores";
	import Purchase from "../../../general-components/purchase.svelte";
    

    let purchasables = [];
    let loading = false;

    const _getPurchasables = async () => {
        loading = true;
        purchasables = await getPurchasables();
        loading = false;
    };

    const _makePurchase = async (p) => {
        if (p.isPremium && !$userStore.isPremium) {
            pushPopup({
                status: 0,
                message: "You must be a premium user to purchase this item."
            });
            return;
        }
        pushPopup({
            status: 2,
            message: `Are you sure you want to purchase ${p.name} for ${p.cost}?`,
            onOk: async() => {
                loading = true;
                const res = await makePurchase(p._key);
                if (res) {
                    pushPopup({
                        status: 1,
                        message: "Purchase successful!",
                        onOk: _getPurchasables
                    })
                }
                loading = false;
            }
        });
    };

    onMount(_getPurchasables);
</script>

<div class="{largeTitle} pb-2">
    Shop
    <div class="flex justify-center text-sm font-normal mt-1">
        {$userStore.points} Points Available
    </div>
</div>

<hr class="{hr}"/>

{#if loading}
    <Loading/>
{:else if !purchasables.length}
    <div class="flex gap-2">
        <div>No available purchases</div>
    </div>
{:else}
    <div class="{gridContainer}">
        {#each purchasables as p, i}
            <Purchase
                p={p}
                onClick={() => _makePurchase(p)}
            />
        {/each}
    </div>
{/if}