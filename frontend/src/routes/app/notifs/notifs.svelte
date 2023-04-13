<script>
    import { onMount } from 'svelte';
    
    import Notif from './notif.svelte';
    import Loading from '../../../general-components/loading.svelte';
	
    import { acceptFriend, loadNotifications, rejectFriend } from '../../../requests/friend';	
	import { largeTitle, listItem } from '../../../css';
	import { userStore } from '../../../stores';

    let notifs = [];
    let loading = true;

    const _acceptFriend = async(i, friendshipKey) => {
        console.log({i, friendshipKey})
        const success = await acceptFriend(friendshipKey);
        if (success) {
            notifs.splice(i, 1);
            notifs = notifs;
        }
    }

    const _rejectFriend = async(i, friendshipKey) => {
        console.log({i, friendshipKey})
        const success = await rejectFriend(friendshipKey);
        if (success) {
            notifs.splice(i, 1);
            notifs = notifs;
        }
    }

    const _closeJoin = async(i) => {
        if (success) {
            notifs.splice(i, 1);
            notifs = notifs;
        }
    }

    const _joinGame = async(lobbyInput) => {
        loading = true;
        const res = await Game.join(lobbyInput);
        console.log("Err:", res);
        loading = false;
    }

    onMount(async() => {
        if (!$userStore) return;
        notifs = await loadNotifications();
        notifs.push(await loadFriendsInGameNotifs());
        loading = false;
    });
</script>

<div class="{largeTitle}">
    Your Notifications
</div>

{#if loading}
    <Loading/>
{:else}
    <div class="rounded h-full overflow-auto p-2">
        <ul
            tabindex="-1"
            role="listbox"
            aria-labelledby="listbox-label"
            aria-activedescendant="listbox-option-3"
        >
            {#if notifs.length}
                {#each notifs as n, i}
                    <Notif
                        n={n}
                        acceptFriend={() => _acceptFriend(i, n.key)}
                        rejectFriend={() => _rejectFriend(i, n.key)}
                        closeJoin={() => _closeJoin(i)}
                        joinGame={() => _joinGame(lobbyInput)}
                    />
                {/each}
            {:else}
                <li class="{listItem}">
                    You have no notifications.
                </li>
            {/if}
        </ul>
    </div>
{/if}