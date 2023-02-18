<script>
    import axios from 'axios';
    import { PUBLIC_BACKEND_API } from '$env/static/public';
	import { onMount } from 'svelte';
    import { userStore } from '../../stores';
    import Notif from './notif.svelte';
	import AccountBar from '../account-bar.svelte';

    let notifs = [];

    const acceptFriend = async(i, friendshipKey) => {
        console.log({i, friendshipKey})
        axios.post(
            PUBLIC_BACKEND_API + 'user/accept-friend/',
            {
                key: friendshipKey
            }
        ).then(() => {
            notifs.splice(i, 1);
            notifs = notifs;
        }).catch((err) => {
            console.log(err);
        });
    }

    const rejectFriend = async(i, friendshipKey) => {
        axios.post(
            PUBLIC_BACKEND_API + 'user/reject-friend/',
            {
                key: friendshipKey
            }
        ).then(() => {
            notifs.splice(i, 1);
            notifs = notifs;
        }).catch((err) => {
            console.log(err);
        });
    }

    const processPending = (pendingRes) => {
        const pendingList = pendingRes?.data?.pending || [];
        pendingList.forEach(
            x => x.title = 'Incoming Friend Request'
        );
        return pendingList;
    }

    const loadNotification = () => {
        Promise.all([
            axios.post(
                PUBLIC_BACKEND_API + 'user/pending-friends/',
                {
                    id: $userStore.id
                }
            )
        ]).then(([ pendingRes ]) => {
            notifs = [
                ...processPending(pendingRes)
            ];
            notifs.sort((a, b) => b.timestamp - a.timestamp);
            console.log(notifs)
        }).catch((err) => {
            console.log(err)
        });
    }

    loadNotification();
</script>

<div class="my-4 text-2xl text-center font-bold text-gray-700">
    Your Notifications
</div>

<div
    class="rounded h-full p-2 overflow-auto"
    style="height: calc(100% - 62px)"
>
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
                    acceptFriend={() => acceptFriend(i, n.friendshipKey)}
                    rejectFriend={() => rejectFriend(i, n.friendshipKey)}
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
