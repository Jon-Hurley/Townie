<script>
	import { goto } from '$app/navigation';
	import { userStore } from '../../stores';
	import { logout } from '../../requests/account';
	import Username from '../../general-components/username.svelte';
	import Premium from '../../general-components/premium.svelte';

	$: pages = [
		{
			page: '/app/account/',
			tooltip: 'Account',
			styles: 'text-indigo-500 w-full bg-gray-100 p-1',
			svg: 'M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z',
            text: 'username',
            svgStyle: 'hover:scale-125 transition-scale duration-200 m-1 mr-3'
		},
        {
			Component: Premium,
            styles: 'hover:bg-gray-100 p-1 ml-4 hover:scale-125 transition-scale duration-200',
            tooltop: 'Premium'
        },
        {
			page: '/logout',
			styles: 'text-gray-500 hover:scale-125 hover:bg-gray-100 p-1 ml-4',
			tooltip: 'Logout',
			svg: 'M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75'
		}
	];
</script>

<nav
	class="
        w-full p-4 h-[60px] min-h-[60px]
        flex items-center justify-between
        overflow-hidden
        border-b-[1px] border-gray-500 
    "
>
	{#each pages as { Component, page, tooltip, svg, text, styles, svgStyle, onClick }}
        {#if Component}
            <div
                class="
                    flex items-center rounded-full
                    transition duration-150 ease-in-out
                    transition-scale duration-200
                    {styles}
                "
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title={tooltip}
            >
                <Component/>
            </div>
        {:else}
            <button
                type="button"
                class="
                    rounded-full
                    transition-scale duration-200
                    transition duration-150 ease-in-out
                    flex items-center
                    {styles}
                "
                data-bs-toggle="tooltip"
                data-bs-placement="top"
                title={tooltip}
                on:click={() => {
                    if (onClick) {
                        onClick();
                        return;
                    }
                    if (page === '/logout') {
                        logout();
                        return;
                    }
                    goto(page);
                }}
            >
                <svg
                    class="h-7 w-7 {svgStyle}"
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
                    <div class="text-2xl font h-[33px]">
                        {#if text === 'username'}
                            <Username/>
                        {:else if text}
                            {text}
                        {/if}
                    </div>
                {/if}
            </button>
        {/if}
	{/each}
</nav>