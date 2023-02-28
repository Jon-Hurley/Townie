<script>
	import '../app.css';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { pages, getHighlight } from './navbar';

    let currentPage;
    let highlightedPage;

    page.subscribe(v => {
        currentPage = v.route.id;
        console.log(currentPage)
        highlightedPage = getHighlight(currentPage);
    });
</script>

{#if highlightedPage}
    <nav
        class="
            absolute
            bottom-0
            bg-gray-800
            w-full
            px-2
            h-14
            flex
            items-center
            justify-around overflow-hidden
        "
    >
        {#each pages as { page, tooltip, svg }}
            <button
                type="button"
                class="
                    rounded-full
                    p-8
                    text-gray-400 
                    hover:text-white
                    transition-colors duration-500
                    transition duration-150 ease-in-out
                    {highlightedPage == page ? 'bg-indigo-700' : 'hover:bg-indigo-700'}
                "
                data-bs-toggle="tooltip" 
                data-bs-placement="top"
                title={tooltip}

                on:click={() => {
                    if (page === '/login') {
                        // logout();
                    }
                    goto(page);
                }}
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
        {/each}
    </nav>
{/if}