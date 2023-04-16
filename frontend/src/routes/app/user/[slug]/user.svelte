<script>
	import { acceptFriend, rejectFriend, sendFriendRequest } from "../../../../requests/friend";
	import { userStore } from "../../../../stores";
    import { buttonStyle, redStyle, greenStyle, blueStyle, hr, gridContainer } from '../../../../css'
	import Username from "../../../../general-components/username.svelte";
	import Purchase from "../../../../general-components/purchase.svelte";
	
    const title = "text-gray-700 font-semibold text-lg mt-6";

    export let user, reloadUser;

    const _acceptFriend = async() => {
        const success = await acceptFriend(user.friendship[0].key);
        reloadUser();
    };

    const _rejectFriend = async() => {
        const success = await rejectFriend(user.friendship[0].key);
        reloadUser();
    };

    const _sendFriendRequest = async() => {
        const res = await sendFriendRequest(user.key);
        reloadUser();
    };

    const getNetworkDistanceStr = () => {
        const dist = user.networkDistance;
        switch (dist) {
            case 1: return "1st";
            case 2: return "2nd";
            case 3: return "3rd";
            case 4: return "4th";
            default: return "5th+";
        }
    };
</script>

<div class="my-5 w-full pb-4">
    <div class="text-gray-700 font-bold text-3xl text-center">
        <Username boldness={'bold'} user={user}/>
    </div>
    <div class="text-gray-700 text-md text-center mt-1">
        {getNetworkDistanceStr()} &bull;  
        {user.mutualFriends} Mutual Friend{user.mutualFriends == 1 ? '' : 's'}
    </div>
</div>

{#if user.key !== $userStore.key}
    <div class="flex justify-center flex-wrap">
        <!-- <button
            disabled
            class="{indigoStyle} {buttonStyle} m-1"
        >
            Message
        </button> -->

        {#if !user?.friendship}
            <button
                class="{blueStyle} {buttonStyle} m-1"
                on:click={_sendFriendRequest}
            >
                Send Friend Request
            </button>
        {:else if user.friendship.status}
            <button
                class="{redStyle} {buttonStyle} m-1"
                on:click={_rejectFriend}
            >
                Remove Friend
            </button>
        {:else if user.friendship.inbound}
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
    Purchases
</div>
<hr class={hr}>
{#if user?.purchases?.length}
    <div class="{gridContainer}">
        {#each user?.purchases as p}
            <Purchase p={p}/>
        {/each}
    </div>
{:else}
    <div class="flex gap-2">
        <div>You have no purchases</div>
    </div>
{/if}
