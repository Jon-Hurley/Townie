<script>
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { pages, getHighlight } from './navbar';
    import Icon from '$lib/assets/townie-icon.jpg';

    let currentPage;
    let highlightedPage;

    page.subscribe(v => {
        currentPage = v.route.id;
        highlightedPage = getHighlight(currentPage);
    });
</script>

<div
    class="
        bg-gray-800
        w-screen
        h-[60px] min-h-[60px]
        flex items-center justify-around
        z-50
    "
>
    {#each pages as { page, tooltip, svg }, i}
        {#if i == 2}
            <button
                type="button"
                class="
                    rounded-full p-4 mb-6
                    transition-colors duration-500 transition duration-150 ease-in-out
                    ring-4 ring-white
                    border-4 border-indigo-700
                "
                style="
                    background-image: url({Icon});
                    width: 55px;
                    height: 55px;
                    background-size: cover;
                "
                data-bs-toggle="tooltip" 
                data-bs-placement="top"
                title={tooltip}
                on:click={() => goto(page)}
            />
        {:else}
            <button
                type="button"
                class="
                    rounded-full p-4
                    transition-colors duration-500 transition duration-150 ease-in-out
                    {highlightedPage === page ? 
                        'text-white bg-indigo-700'
                        : 'text-gray-400 hover:text-white hover:bg-indigo-700'
                    }
                "
                data-bs-toggle="tooltip" 
                data-bs-placement="top"
                title={tooltip}
                on:click={() => goto(page)}
            >
                <svg
                    class="h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                >
                    <path d={svg}/>
                </svg>
            </button>
        {/if}
    {/each}
</div>