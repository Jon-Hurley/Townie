<script>	
    import Username from "../../../../general-components/username.svelte";

    import { acceptFriend, rejectFriend, sendFriendRequest } from "../../../../requests/friend";
	import { userStore } from "../../../../stores";
    import { buttonStyle, redStyle, greenStyle, blueStyle, hr, largeTitle } from '../../../../css';	
	import { pointsToLevel, pointsToProgress, pointsToRank } from "../../../../util";
    import Purchase from "../../../../general-components/purchase.svelte";
    import { gridContainer } from "../../../../css";
    const title = "text-gray-700 font-semibold text-lg mt-6";

	export let user, reloadUser, rank;

    const _acceptFriend = async() => {
        const success = await acceptFriend(user.friendship.key);
        reloadUser();
    };

    const _rejectFriend = async() => {
        const success = await rejectFriend(user.friendship.key);
        reloadUser();
    };

    const _sendFriendRequest = async() => {
        const res = await sendFriendRequest(user.key);
        reloadUser();
    };

    const getNetworkDistanceStr = () => {
        const dist = user.networkDistance;
        switch (dist) {
            case 0: return "0th";
            case 1: return "1st";
            case 2: return "2nd";
            case 3: return "3rd";
            case 4: return "4th";
            default: return "5th+";
        }
    };
</script>

<div class="{largeTitle} pb-4">
    <div class="flex justify-center">
        <Username boldness={'bold'} user={user}/>
        {#if user.inGame}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-green-600">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.893 13.393l-1.135-1.135a2.252 2.252 0 01-.421-.585l-1.08-2.16a.414.414 0 00-.663-.107.827.827 0 01-.812.21l-1.273-.363a.89.89 0 00-.738 1.595l.587.39c.59.395.674 1.23.172 1.732l-.2.2c-.212.212-.33.498-.33.796v.41c0 .409-.11.809-.32 1.158l-1.315 2.191a2.11 2.11 0 01-1.81 1.025 1.055 1.055 0 01-1.055-1.055v-1.172c0-.92-.56-1.747-1.414-2.089l-.655-.261a2.25 2.25 0 01-1.383-2.46l.007-.042a2.25 2.25 0 01.29-.787l.09-.15a2.25 2.25 0 012.37-1.048l1.178.236a1.125 1.125 0 001.302-.795l.208-.73a1.125 1.125 0 00-.578-1.315l-.665-.332-.091.091a2.25 2.25 0 01-1.591.659h-.18c-.249 0-.487.1-.662.274a.931.931 0 01-1.458-1.137l1.411-2.353a2.25 2.25 0 00.286-.76m11.928 9.869A9 9 0 008.965 3.525m11.928 9.868A9 9 0 118.965 3.525" />
            </svg>
        {:else}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-red-600">
                <path stroke-linecap="round" stroke-linejoin="round" d="M20.893 13.393l-1.135-1.135a2.252 2.252 0 01-.421-.585l-1.08-2.16a.414.414 0 00-.663-.107.827.827 0 01-.812.21l-1.273-.363a.89.89 0 00-.738 1.595l.587.39c.59.395.674 1.23.172 1.732l-.2.2c-.212.212-.33.498-.33.796v.41c0 .409-.11.809-.32 1.158l-1.315 2.191a2.11 2.11 0 01-1.81 1.025 1.055 1.055 0 01-1.055-1.055v-1.172c0-.92-.56-1.747-1.414-2.089l-.655-.261a2.25 2.25 0 01-1.383-2.46l.007-.042a2.25 2.25 0 01.29-.787l.09-.15a2.25 2.25 0 012.37-1.048l1.178.236a1.125 1.125 0 001.302-.795l.208-.73a1.125 1.125 0 00-.578-1.315l-.665-.332-.091.091a2.25 2.25 0 01-1.591.659h-.18c-.249 0-.487.1-.662.274a.931.931 0 01-1.458-1.137l1.411-2.353a2.25 2.25 0 00.286-.76m11.928 9.869A9 9 0 008.965 3.525m11.928 9.868A9 9 0 118.965 3.525" />
            </svg>
        {/if}
          
    </div>
    <div class="text-sm font-normal mt-1">
        {pointsToRank(user?.cumPoints)} &bull;
        {getNetworkDistanceStr()} &bull;
        {user.mutualFriends} Mutual Friend{user.mutualFriends == 1 ? '' : 's'}
    </div>
</div>


{#if user.key !== $userStore.key}
    <div class="flex justify-center flex-wrap">
        <!-- <button
            disabled
            class="text-{$primaryColor}-500 border-{$primaryColor}-500 {buttonStyle} m-1"
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
	Level {pointsToLevel(user?.cumPoints)}
</div>
<hr class={hr} />
<meter
	id="xp-meter"
	class="h-8 w-full px-2 shimmer"
	min="0"
	max="1"
	value={pointsToProgress(user?.cumPoints)}
/>

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