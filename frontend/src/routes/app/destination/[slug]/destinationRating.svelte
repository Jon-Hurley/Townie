<script>
	import Rating from '../../../../general-components/rating.svelte';

    import { pushPopup } from '../../../../stores';
	import { submitDestRating } from '../../../../requests/account';
    import { hr } from '../../../../css';
    const title = 'font-semibold text-lg mt-6';

	export let destination, initialUserRating, showRateable, reload;

	const _submitDestRating = async (userRating) => {		
		const success = await submitDestRating(destination._key, userRating);
		if (success) {
			pushPopup({
				status: 1,
				message: 'Your rating has been received',
				onOk: reload
			});
		}
	};

    $: _destRating = !destination?.numRatings ? 0 : destination?.ratingPoints / destination?.numRatings;
    $: destRating = Math.round(_destRating * 10) / 10;
</script>

<div class="{title}">
    Rating
</div>
<hr class={hr} />

<div class="flex justify-between items-center px-2">
    <div class="mr-2">
        User Rating:
    </div>

    <div class="flex items-center w-60 justify-between">
        <div class="mr-2 flex text-amber-400">
            {#each [1, 2, 3, 4, 5] as star}
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill={star <= destRating ? 'currentColor' : 'none'}
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
            ({destRating} / 5.0)
        </div>
    </div>
</div>

{#if showRateable}
    <Rating
        initialUserRating={initialUserRating}
        onSubmit={_submitDestRating}
    />
{/if}