<script>
    export let n, acceptFriend, rejectFriend;

    const buttonStyle = `
        p-1 m-1 ml-2

        border-2 rounded
        font-medium text-xs
        
        hover:bg-black hover:bg-opacity-5
        focus:outline-none focus:ring-0
        
        transition duration-150 ease-in-out
    `;
</script>

<li
    class="
        bg-white text-gray-900
        mb-2 p-3 w-full
        border-gray-200 border-2 rounded

        cursor-pointer        

        flex justify-between items-center
    "
>
    <div>
        <div
            class="font-semibold mb-1"
        >
            {n.title}
        </div>
        <a href={"/user/" + n.friend.key}>
            {n.friend.username} #{n.friend.key}
        </a>
    </div>

    <div class="flex">
        {#if n.title === 'Incoming Friend Request'}
            <button
                type="button"
                class="
                    border-green-500
                    text-green-500
                    ${buttonStyle}
                "
                on:click={acceptFriend}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
            </button>
            <button
                type="button"
                class="
                    border-red-500
                    text-red-500                    
                    ${buttonStyle}
                "
                on:click={rejectFriend}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        {:else if n.title === 'Outgoing Friend Request'}
            <button
                type="button"
                class="
                    border-red-500
                    text-red-500                    
                    ${buttonStyle}
                "
                on:click={rejectFriend}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        {/if}
    </div>
</li>