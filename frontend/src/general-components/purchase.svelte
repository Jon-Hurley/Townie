<script>
	import { primaryColor } from "../stores";

    export let p, onClick = () => {}, isActive = true;
</script>

<button
    class="
        border-[2px] border-{p?.isPremium ? $primaryColor : 'gray'}-500
        rounded-2xl
        w-24 h-24
        relative
        opacity-{isActive ? '100' : '25'}
    "
    on:click={onClick}
>
    <div class="absolute top-[-0.75rem] flex w-full justify-center">
        <div class="text-sm bg-white px-1">
            {p?.category}
        </div>
    </div>

    <div class="font-semibold text-lg">
        {p?.name}
    </div>
    <div class="text-sm">
        {p?.cost} pts
    </div>

    {#if p?.isPremium}
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1792 1792"
            class="
                absolute
                bottom-[-0.75rem]
                bg-white
                w-6 h-6
                text-{$primaryColor}-500
            "
            style="left: calc(50% - 0.75rem)"
        >
            <path
                d="m185.546 736.058 545.09 581.837-262.483-581.837H185.546zM896 1411.514l305.355-675.456h-610.71zM470.778 624.066l178.488-335.979H420.031L168.047 624.066h302.73zm590.586 693.83 545.09-581.838h-282.607zm-463.72-693.83h596.712l-178.489-335.979H776.133zm723.578 0h302.73L1371.97 288.087h-229.235zm123.367-425.223 335.978 447.971q12.25 15.75 11.375 36.31-.875 20.561-14.874 35.435l-839.946 895.942Q921.373 1632 896 1632q-25.373 0-41.122-17.499L14.932 718.56Q.933 703.685.058 683.124q-.875-20.56 11.375-36.31l335.978-447.97q15.749-22.75 44.622-22.75h1007.934q28.873 0 44.622 22.75z"
                fill="currentColor"
            />
        </svg>
    {/if}
</button>