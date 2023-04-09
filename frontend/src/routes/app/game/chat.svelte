<script>
	import { onDestroy, onMount } from "svelte";
	import { Game } from "../../../classes/Game";
	import { blueStyle, buttonStyle, grayStyle, hr, inputStyle, largeTitle } from "../../../css";
	import { userStore } from "../../../stores";
    let messages = Game.messageStore;
    $: console.log($messages);
    
    let input;
    let isOpen = false;
    let scrollElement;  

    const sendMessage = () => {
        if (!input?.length) return;
        Game.send('new-message', {
            message: {
                key: $userStore.key,
                username: $userStore.username,
                message: input,
                timestamp: new Date().toLocaleTimeString()
            },
            connectionIds: Game.players.map(x => x.connectionId)
        });
        input = null;
    }

    let timeout;
    $: $messages, () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            if (!scrollElement) return;
            scrollElement.scroll({
                top: scrollElement.scrollHeight,
                behavior: 'smooth'
            });
        }, 1000);
    };
    onDestroy(() => clearTimeout(timeout));
</script>

<button
    type="button"
    class="{buttonStyle} {blueStyle}"
    on:click={() => isOpen = true}
>
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" />
    </svg>
</button>

<div
    class="
        fixed inset-0 bg-gray-200 mb-16
        pointer-events-none
        transition-all duration-500
        {isOpen ? 'bg-opacity-75' : 'bg-opacity-0'}
    "
/>

<div
    class="
        fixed left-0 bottom-16
        w-screen text-center
        transition-all duration-500
        {isOpen ? 'translate-y-0' : 'translate-y-full pointer-events-none'}
    "
>
    <div
        class="
            bg-gray-50 p-4 rounded-t-lg
            w-full 
        "
    >
        <div class="{largeTitle}">
            Chat
        </div>
        <hr class="{hr} my-4">

        <div
            class="
                p-2 min-h-[50vh] max-h-[50vh]
                flex flex-col gap-2 overflow-scroll
            "
            bind:this={scrollElement}
        >
            {#each $messages as { username, message, timestamp, key }}
                <div class="flex justify-between items-center">
                    {#if $userStore.key === key}
                        <div class="text-sm font-light">{timestamp}</div>
                        <div class="
                                flex flex-col p-2 px-4 bg-indigo-300
                                rounded-bl-2xl rounded-tr-2xl rounded-tl-2xl
                                text-right
                            "
                        >
                            <div class="font-bold">{username}</div>
                            <div class="text-sm">{message}</div>
                        </div>
                    {:else}
                        <div class="
                                flex flex-col p-2 px-4 bg-gray-200
                                rounded-br-2xl rounded-tr-2xl rounded-tl-2xl
                                text-left
                            "
                        >
                            <div class="font-bold">{username}</div>
                            <div class="text-sm">{message}</div>
                        </div>
                        <div class="text-sm font-light">{timestamp}</div>
                    {/if}
                </div>
            {/each}
        </div>
        
        <form class="flex gap-2 mt-4" on:submit={sendMessage}>
            <input
                bind:value={input}
                class="{inputStyle}"
                placeholder="Type a message..."
                on:enter
            />
            <button
                class="{buttonStyle} {blueStyle}"
                on:click={sendMessage}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                </svg>
            </button>
        </form>

        <hr class="{hr} my-4" />
		<div class="flex ">
			<button
				class="{buttonStyle} {grayStyle} w-full"
				on:click={() => isOpen = false}
			>
				Cancel
			</button>
		</div>
    </div>
</div>