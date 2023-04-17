<script>
	import { greenStyle, redStyle, buttonBaseStyle, listItem, indigoStyle } from "../../../css";
	import Username from "../../../general-components/username.svelte";

    export let n, joinGame, closeJoin;

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
        <a href={"/app/user/" + n.friend.key}>
            <Username user={n.friend}/>
        </a>
    </div>

    <div class="flex">
        {#if n.title === 'Join game'}
            <button
                type="button"
                class="{indigoStyle} {buttonStyle}"
                on:click={joinGame}
            >
            Join
            </button>
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