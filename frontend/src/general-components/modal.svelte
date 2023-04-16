<script>
	import { amberStyle, buttonStyle, grayStyle, greenStyle, redStyle } from '../css';

	export let
		status = 0,
		message = '',
		onOk = () => {},
		onCancel = () => {},
		okText = 'Ok',
		cancelText = 'Cancel',
		includeCancel = status === 2;  // typically only confirmations have a cancel button

	const colorStyle = [redStyle, greenStyle, grayStyle, amberStyle][status];
	const color = ['red', 'green', 'gray', 'amber'][status];
	const name = ['Error', 'Success', 'Confirm', 'Warning'][status];
	const bStyle = `${buttonStyle} ${colorStyle}`;
	const svg = [
		'M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z',
		'M4.5 12.75l6 6 9-13.5',
		'M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z',
		'M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z'
	][status];
</script>

<div class="z-50 fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full">
	<div
		class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700"
	>
		<div class="mt-3 text-center">
			<div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-{color}-100">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					class="w-8 h-8 text-{color}-500"
				>
					<path stroke-linecap="round" stroke-linejoin="round" d={svg} />
				</svg>
			</div>

			<h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">
				{name}
			</h3>
			<div class="px-4 mt-2 text-left">
				{#each message.split('\n') as str}
					<p class="text-sm text-gray-500">
						{str}
					</p>
				{/each}
			</div>

			<div class="flex gap-2">
				{#if includeCancel}
					<button id="cancel-btn" on:click={onCancel} class="w-full mt-6 {buttonStyle} {redStyle}">
						{cancelText}
					</button>
				{/if}

				<button id="ok-btn" on:click={onOk} class="w-full mt-6 {buttonStyle} {bStyle}">
					{okText}
				</button>
			</div>
		</div>
	</div>
</div>
