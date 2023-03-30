<script>
	import { buttonStyle, greenStyle, redStyle } from '../css';

	export let status, message, onOk;
</script>

<div
	class="z-50 fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full"
	id="error-popup"
>
	<div
		class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700"
	>
		<div class="mt-3 text-center">
			{#if status === 1}
				<div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-green-100">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-8 h-8 text-green-500"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
					</svg>
				</div>
			{:else}
				<div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-red-100">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-14 h-14 text-red-500"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
						/>
					</svg>
				</div>
			{/if}

			<h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">
                {status === 1 ? 'Success' : 'Error'}
            </h3>
			<div class="px-7">
				<p class="text-sm text-gray-500">
					{message}
				</p>
			</div>

			<button
				id="ok-btn"
				on:click={onOk}
				class="w-full mt-6 {buttonStyle} {status === 1 ? greenStyle : redStyle}"
			>
				OK
			</button>
		</div>
	</div>
</div>
