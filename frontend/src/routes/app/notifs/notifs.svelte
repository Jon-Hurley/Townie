<script>
    import { onMount } from 'svelte';
    
    import { goto } from '$app/navigation';
    import Notif from './notif.svelte';
    import Loading from '../../../general-components/loading.svelte';
	
    import { acceptFriend, loadNotifications, rejectFriend } from '../../../requests/friend';	
	import { hr, largeTitle, listItem } from '../../../css';
	import { pushPopup, userStore } from '../../../stores';
	import { Game } from '../../../classes/Game';

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
        notifs.splice(i, 1); // DOES NOT CLOSE THE RIGHT NOTIFS
        notifs = notifs;
    }

    const _joinGame = async(lobbyInput) => {
        pushPopup({
            status: 2,
            message: "Are you sure about that?",
            onOk: async() => {
                const success = await Game.join(lobbyInput);
                if (success) {
                    goto('/app/game');
                }
            }
        });
    }

    onMount(async() => {
        if (!$userStore) return;
        notifs = await loadNotifications();
        console.log({notifs})
        loading = false;
    });
</script>

<div class="{largeTitle}">
    Your Notifications
</div>
<hr class="{hr}"/>

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
                        joinGame={() => _joinGame(n.gameKey)}
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