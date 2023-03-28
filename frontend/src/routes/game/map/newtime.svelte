<script>
    import { onMount } from 'svelte';
    import { blueStyle, buttonStyle, grayStyle, hr, largeTitle, inputStyle } from '../../../css';
	import { Game } from '../../../Game';

    let form = {};

    let popup = false;

    let update = false;
    
    onMount(() => {
        Game.store.subscribe(gs => {
            if (gs) {
                form = { ...gs.game.settings };
                form.otherCompletionTime = form.otherCompletionTime;
            }
        })
    })

    let otherCompletionTime = false;

    const _updateTime = () => {
        Game.updateTime(form);
    };
</script>


<label>
    <input type=checkbox bind:checked={update}>
    Change the time frame for your game!
</label>

{#if update}
    <div
        class="
            flex justify-between items-center
            bg-white p-3 mb-2
            border-2 border-gray-200 rounded
        "
        >
        <div class="font-semibold">
            Length
        </div>
        <select
            on:change={e => {
                const v = e.target.value;
                otherCompletionTime = v === "Other";
                if (!otherCompletionTime) {
                    form.desiredCompletionTime = parseInt(v);
                }
            }}
            value={form.desiredCompletionTime}
            class="w-40"
        >
            <option value={30}>30 minutes</option>
            <option value={60}>60 minutes</option>
            <option value={90}>90 minutes</option>
            <option value={120}>120 minutes</option>
            <option value={180}>180 minutes</option>
            <option value="Other">Other</option>
        </select>

        {#if otherCompletionTime}
            <input
                class="w-40"
                placeholder="Other"
                type="number"
                min="1"
                value={form.desiredCompletionTime}
                on:input={e => {
                    let v;
                    try {
                        v = parseInt(e.target.value)
                    } catch (err) {
                        v = 0;
                    }
                    form.desiredCompletionTime = Math.abs(v);
                }}
            />
        {/if}
        <button
                class="{buttonStyle} {blueStyle}"
                on:click={() => {
                    update = false;
                    _updateTime()
                }}
            >
                Save new time
            </button>
    </div>
    
{/if}

