<script>
	import { pushPopup } from '../../../../stores';
	import { indigoStyle, hr } from '../../../../css';
	import { submitRating } from '../../../../requests/account';
    const title = 'font-semibold text-lg mt-6';

	export let summary, userInGame, reloadGameSummary;

    let userRating = summary?.userRating?.rating || 0;

	const _submitRating = async () => {
		if (userRating > 5 || userRating < 0) {
			pushPopup({
				status: 0,
				message: 'Please select a valid rating to submit.'
			});
			return;
		}
        
		const success = await submitRating(
            summary?.theme?._key,
            userRating
        );
		if (success) {
            pushPopup({
                status: 1,
                message: 'Your rating has been submitted!',
                onOk: reloadGameSummary
            });
        }
	};

    $: _themeRating = !summary?.theme?.numRatings ?
        0 : summary?.theme?.ratingPoints / summary.theme.numRatings;
    $: themeRating = Math.round(_themeRating * 10) / 10;
</script>

<div class="{title}">
    Theme
</div>
<hr class={hr} />

<div class="flex justify-between items-center px-2">
    <div class="mr-2">
        Name: {summary.game.settings.theme}
    </div>

    <div class="flex items-center w-60 justify-between">
        <div class="mr-2 flex text-amber-400">
            {#each [1, 2, 3, 4, 5] as star}
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill={star <= themeRating ? 'currentColor' : 'none'}
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke='black'
                    class="w-6 h-6 cursor-pointer"
                >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                </svg>
            {/each}
        </div>

        <div>
            ({themeRating} / 5.0)
        </div>
    </div>
</div>

{#if userInGame}
    <div class="flex justify-between items-center mt-4 px-2">
        <div class="mr-2">
            Submit Rating:
        </div>

        <div class="flex items-center w-60 justify-between">
            <div class="flex text-amber-400 mr-2">
                {#each [1, 2, 3, 4, 5] as star}
                    <button on:click={() => userRating = star}>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill={star <= userRating ? 'currentColor' : 'none'}
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke='black'
                            class="w-6 h-6 cursor-pointer"
                        >
                            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                        </svg>
                    </button>
                {/each}
            </div>

            <button
                class="
                    border-2 py-1 px-3 rounded-full
                    {indigoStyle} hover:scale-105
                "
                on:click={_submitRating}
            >
                Submit
            </button>
        </div>
    </div>
{/if}