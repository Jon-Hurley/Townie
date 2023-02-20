<script>
    import Notif from './notif.svelte';
	import { acceptFriend, loadNotifications, rejectFriend } from '../../requests/friend';
	import { onMount } from 'svelte';

    let notifs = [];

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
    });
</script>

<div class="my-4 text-2xl text-center font-bold text-gray-700">
    Your Notifications
</div>

<div class="rounded h-full overflow-auto">
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
                    acceptFriend={() => _acceptFriend(i, n.friendshipKey)}
                    rejectFriend={() => _rejectFriend(i, n.friendshipKey)}
                />
            {/each}
        {:else}
            <li
                class="
                    bg-white
                    mb-2
                    p-2
                    rounded

                    border-gray-200
                    border-2

                    w-full
                    text-gray-900
                    relative
                    cursor-default
                    select-none
                "
            >
                You have no notifications.
            </li>
        {/if}
    </ul>
</div>