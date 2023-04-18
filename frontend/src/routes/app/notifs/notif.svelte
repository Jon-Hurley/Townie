<script>
	import { greenStyle, redStyle, indigoStyle, buttonBaseStyle, listItem } from "../../../css";
	import Username from "../../../general-components/username.svelte";

    export let n, acceptFriend, rejectFriend, joinGame, closeJoin;

    const buttonStyle = `
        p-1 m-1 ml-2 text-xs
        border-2 rounded
        ${buttonBaseStyle}
    `;
</script>

<li class="{listItem}">
    <div class="text-left">
        <div class="font-semibold mb-1">
            {n.title}
        </div>

        {#if n.title === 'Your friend is in a game'}
            <a href={"/app/user/" + n.key}>
                <Username user={n}/>
            </a>
        {:else}
            <a href={"/app/user/" + n.friend.key}>
                <Username user={n.friend}/>
            </a>
        {/if}
    </div>

    <div class="flex">
        {#if n.title === 'Incoming Friend Request'}
            <button
                type="button"
                class="{greenStyle} {buttonStyle}"
                on:click={acceptFriend}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
            </button>
            <button
                type="button"
                class="{redStyle} {buttonStyle}"
                on:click={rejectFriend}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        {:else if n.title === 'Outgoing Friend Request'}
            <button
                type="button"
                class="{redStyle} {buttonStyle}"
                on:click={rejectFriend}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        {:else if n.title === 'Your friend is in a game'}
            {#if n.gameKey}
                <button
                    type="button"
                    class="{indigoStyle} px-3 py-1 m-1 ml-2 text-sm
                    border-2 rounded
                    ${buttonBaseStyle}"
                    on:click={joinGame}
                >
                    Join
                </button>
            {/if}
            
            <button
                type="button"
                class="{redStyle} {buttonStyle}"
                on:click={closeJoin}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        {/if}
    </div>
</li>