<script>
	import { buttonStyle, indigoStyle } from '../css';
	import { initiatePremiumSession } from '../requests/store';
	import { primaryColor, userStore } from '../stores';

    export let simplified = true;

    const _initiatePremiumSession = async() => {
        const url = await initiatePremiumSession();
    }

    const _openStripePortal = async() => {
        const winder = window.open('https://billing.stripe.com/p/login/8wM6pUbE3eFz20UeUU', '_blank');
        if (winder?.focus) winder.focus();
    }

    $: isPremium = !!$userStore?.isPremium;
    $: handleClick = isPremium ? _openStripePortal : _initiatePremiumSession;
</script>

{#if simplified}
    <button
        on:click={handleClick}
        title={isPremium ? 'Manage Premium' : 'Upgrade to Premium'}
    >
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1792 1792"
            width="26"
            height="26"
            class="m-[1px] mt-[2px]"
        >
            <path
                d="m185.546 736.058 545.09 581.837-262.483-581.837H185.546zM896 1411.514l305.355-675.456h-610.71zM470.778 624.066l178.488-335.979H420.031L168.047 624.066h302.73zm590.586 693.83 545.09-581.838h-282.607zm-463.72-693.83h596.712l-178.489-335.979H776.133zm723.578 0h302.73L1371.97 288.087h-229.235zm123.367-425.223 335.978 447.971q12.25 15.75 11.375 36.31-.875 20.561-14.874 35.435l-839.946 895.942Q921.373 1632 896 1632q-25.373 0-41.122-17.499L14.932 718.56Q.933 703.685.058 683.124q-.875-20.56 11.375-36.31l335.978-447.97q15.749-22.75 44.622-22.75h1007.934q28.873 0 44.622 22.75z"
                fill="currentColor"
            />
        </svg>
    </button>
{:else}
    <button
        class="{indigoStyle} {buttonStyle}"
        on:click={handleClick}
    >
        <div class="flex gap-2">
            <div>
                {isPremium ? 'Manage Premium' : 'Upgrade to Premium'}
            </div>
    
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 1792 1792"
                width="24"
                height="24"
                class="text-indigo-500"
            >
                <path
                    d="m185.546 736.058 545.09 581.837-262.483-581.837H185.546zM896 1411.514l305.355-675.456h-610.71zM470.778 624.066l178.488-335.979H420.031L168.047 624.066h302.73zm590.586 693.83 545.09-581.838h-282.607zm-463.72-693.83h596.712l-178.489-335.979H776.133zm723.578 0h302.73L1371.97 288.087h-229.235zm123.367-425.223 335.978 447.971q12.25 15.75 11.375 36.31-.875 20.561-14.874 35.435l-839.946 895.942Q921.373 1632 896 1632q-25.373 0-41.122-17.499L14.932 718.56Q.933 703.685.058 683.124q-.875-20.56 11.375-36.31l335.978-447.97q15.749-22.75 44.622-22.75h1007.934q28.873 0 44.622 22.75z"
                    fill="currentColor"
                />
            </svg>
        </div>
    </button>
{/if}