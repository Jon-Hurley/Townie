<script>
	import '../app.css';
    import { goto } from '$app/navigation';
    import { logout, userStore } from '../stores';
	import { get } from 'svelte/store';
    import { page } from '$app/stores';

    let currentPage;
    page.subscribe(v => currentPage = v.route.id);

    $: pages = [
        {
            page: '/account',
            tooltip: 'Account',
            styles: 'text-indigo-500',
            svg: "M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z",
            text: $userStore.username || 'Invalid User'
        },
        {
            page: '/login',
            styles: 'text-gray-400',
            tooltip: 'Logout',
            svg: "M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"
        }
    ]
</script>

{#if currentPage && !['/login', '/signup'].includes(currentPage)}
    <nav
        class="
            w-full
            p-6
            h-16
            flex
            items-center
            justify-between
            overflow-hidden
            border-b-2
            border-gray-100 
        "
    >
        {#each pages as { page, tooltip, svg, text, styles }}
            <button
                type="button"
                class="
                    rounded-full
                    hover:text-indigo-500
                    transition-colors duration-500
                    transition duration-150 ease-in-out
                    flex items-center
                    {styles}
                "
                data-bs-toggle="tooltip" 
                data-bs-placement="top"
                title={tooltip}
                
                on:click={() => {
                    if (page === '/login') {
                        logout();
                    }
                    goto(page);
                }}
            >
                <svg
                    class="h-8 w-8"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    transform="scale(-1,1)"
                >
                    <path d={svg}/>
                </svg>

                {#if text}
                    <div
                        class="ml-4 text-xl font"
                    >
                        {text}
                    </div>
                {/if}
            </button>
        {/each}
    </nav>
{/if}