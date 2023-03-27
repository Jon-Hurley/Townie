<script>
    import Notif from './notif.svelte';
	import { acceptFriend, loadNotifications, rejectFriend } from '../../requests/friend';
	import { onMount } from 'svelte';
	import Loading from '../../general-components/loading.svelte';
	import { largeTitle, listItem } from '../../css';
	import Modal from '../../general-components/modal.svelte';

    let notifs = [];
    let loading = true;

    let messageObj = {
        status: 0,
        message: null,
        dest: null
    };

    const _acceptFriend = async(i, friendshipKey) => {
        console.log({i, friendshipKey})
        const errorMessage = await acceptFriend(friendshipKey);
        if (errorMessage) {
            messageObj = {
                status: 0,
                message: errorMessage
            };
            return;
        }
        
        notifs.splice(i, 1);
        notifs = notifs;
    }

    const _rejectFriend = async(i, friendshipKey) => {
        console.log({i, friendshipKey})
        const errorMessage = await rejectFriend(friendshipKey);
        if (errorMessage) {
            messageObj = {
                status: 0,
                message: errorMessage
            };
            return;
        }
        
        notifs.splice(i, 1);
        notifs = notifs;
    }

    onMount(async() => {
        notifs = await loadNotifications();
        loading = false;
    });
</script>

<Modal
    {...messageObj}
/>

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