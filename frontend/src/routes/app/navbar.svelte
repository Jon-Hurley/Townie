<script>
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { pages, getHighlight } from './navbar';
	import { primaryColor } from '../../stores';

    $: highlightedPage = getHighlight($page.route.id);
</script>

<div class="fixed bottom-[-90px] z-[100] w-20 h-20">
    <img
        src='/images/anim_written_in_vi.gif'
        class="object-cover"
        alt={''}
        on:error={e => console.log(e)}
    />
</div>

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
            <div class="bg-white ring-4 ring-white mb-6 rounded-t-lg rounded-3xl">
                <button
                    type="button"
                    class="
                        p-4 transition-colors duration-500 transition duration-150 ease-in-out
                        border-4 border-{$primaryColor}-{highlightedPage === page ? '500' : '700'}
                    "
                    style="
                        background-image: url('/images/townie-icon.jpg');
                        width: 55px;
                        height: 55px;
                        background-size: cover;
                        border-radius: 8px 8px 45% 45%;
                    "
                    data-bs-toggle="tooltip" 
                    data-bs-placement="top"
                    title={tooltip}
                    on:click={() => goto(page)}
                />
            </div>
        {:else}
            <button
                type="button"
                class="
                    rounded-full p-4
                    transition-colors duration-500 transition duration-150 ease-in-out
                    {highlightedPage === page ? 
                        'text-white bg-' + $primaryColor + '-700'
                        : 'text-gray-400 hover:text-white hover:bg-' + $primaryColor + '-700'
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