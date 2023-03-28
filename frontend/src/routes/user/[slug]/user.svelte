<script>
	import { acceptFriend, rejectFriend, sendFriendRequest } from "../../../requests/friend";
	import { userStore } from "../../../stores";
    import { buttonStyle, redStyle, greenStyle, blueStyle, indigoStyle } from '../../../css'
	import Modal from "../../../general-components/modal.svelte";
    const title = "text-gray-700 font-semibold text-lg mt-6";
    const hr = "my-2 bg-gray-100 h-[2px]";

    export let user, reloadUser;

    let messageObj = {
        status: 0,
        message: null,
        dest: null
    };

    const _acceptFriend = async() => {
        const errorMessage = await acceptFriend(user.friendship[0].key);
        if (errorMessage) {
            messageObj = {
                status: 0,
                message: errorMessage
            };
            return;
        }
        reloadUser();
    };

    const _rejectFriend = async() => {
        const errorMessage = await rejectFriend(user.friendship[0].key);
        if (errorMessage) {
            messageObj = {
                status: 0,
                message: errorMessage
            };
            return;
        }
        reloadUser();
    };

    const _sendFriendRequest = async() => {
        const res = await sendFriendRequest(user.key);
        if (res.errorMessage) {
            messageObj = {
                status: 0,
                message: res.errorMessage
            };
            return;
        }
        reloadUser();
    };
</script>


<Modal
    {...messageObj}
/>

<div class="my-5 w-full">
    <div class="text-gray-700 font-bold text-3xl text-center">
        {user.username}
    </div>
    <div class="text-gray-700 text-md text-center">
        #{user.key}
    </div>
</div>


{#if user.key !== $userStore.key}
    <div class="flex justify-center flex-wrap">
        <button
            disabled
            class="{indigoStyle} {buttonStyle} m-1"
        >
            Message
        </button>

        {#if !user?.friendship?.length}
            <button
                class="{blueStyle} {buttonStyle} m-1"
                on:click={_sendFriendRequest}
            >
                Send Friend Request
            </button>
        {:else if user.friendship[0].status}
            <button
                class="{redStyle} {buttonStyle} m-1"
                on:click={_rejectFriend}
            >
                Remove Friend
            </button>
        {:else if user.friendship[0].inbound}
            <button
                class="{greenStyle} {buttonStyle} m-1"
                on:click={_acceptFriend}
            >
                Accept Friend Request
            </button>
            <button
                class="{redStyle} {buttonStyle} m-1"
                on:click={_rejectFriend}
            >
                Reject Friend Request
            </button>
        {:else}
            <button
                class="{redStyle} {buttonStyle} m-1"
                on:click={_rejectFriend}
            >
                Cancel Friend Request
            </button>
        {/if}
    </div>
{/if}


<div class={title}>
    Rank
</div>
<hr class={hr}>
<div class="px-2 py-4 uppercase">
    {user.rank}
</div>


<div class={title}>
    Badges
</div>
<hr class={hr}>
<div class="h-full overflow-auto">
    <div class="flex flex-wrap justify-center gap-2 px-2 py-4">
        {#if !user.purchases.length}
            <div>
                No badges to display.
            </div>
        {/if}
        {#each user.purchases as p}
            <div
                class="
                    border-gray-200 border-4 rounded-full
                    p-3 m-0
                    text-indigo-500 font-semibold
                    w-24 h-24
                    flex flex-col items-center justify-center
                    text-xs
                    hover:scale-110 duration-200
                    z-100
                    overflow-visible
                    cursor-pointer
                "
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d={p.badge}
                    />
                </svg>
            
                {p.name}
            </div>
        {/each}
    </div>
</div>
