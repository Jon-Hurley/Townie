<script>
    import Notif from './notif.svelte';
	import { acceptFriend, loadNotifications, rejectFriend } from '../../requests/friend';
	import { onMount } from 'svelte';
	import Loading from '../../components/loading.svelte';
	import { largeTitle, listItem } from '../../css';

    let notifs = [];
    let loading = true;

    const _acceptFriend = async(i, friendshipKey) => {
        console.log({i, friendshipKey})
        const res = await acceptFriend(friendshipKey);
        if (res) {
            notifs.splice(i, 1);
            notifs = notifs;
        }
    }

    const _rejectFriend = async(i, friendshipKey) => {
        console.log({i, friendshipKey})
        const res = await rejectFriend(friendshipKey);
        if (res) {
            notifs.splice(i, 1);
            notifs = notifs;
        }
    }

    onMount(async() => {
        notifs = await loadNotifications();
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