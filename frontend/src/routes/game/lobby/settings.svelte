<script>
	import { blueStyle, buttonStyle, grayStyle, redStyle } from '../../../css';

	export let settings;
	console.log({ settings });

	let isOpen = false;
</script>

<button type="button" class="{buttonStyle} {grayStyle} w-full" on:click={() => (isOpen = true)}>
	Settings
</button>

<!--
    Background backdrop, show/hide based on modal state.

    Entering: "ease-out duration-300"
    From: "opacity-0"
    To: "opacity-100"
    Leaving: "ease-in duration-200"
    From: "opacity-100"
    To: "opacity-0"
-->

<!--
    Modal panel, show/hide based on modal state.

    Entering: "ease-out duration-300"
        From: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
        To: "opacity-100 translate-y-0 sm:scale-100"
    Leaving: "ease-in duration-200"
        From: "opacity-100 translate-y-0 sm:scale-100"
        To: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
-->

{#if isOpen}
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"/>
    
    <div
        class="
            fixed inset-0
            flex justify-center items-center
            h-full w-full p-4 text-center
        "
    >
        <div class="bg-gray-50 p-3 rounded">
            <div class="flex ">
                <button
                    class="{buttonStyle} {blueStyle} w-full mr-2"
                    on:click={() => {
                        isOpen = false;
                    }}
                >
                    Save
                </button>
                <button 
                    class="{buttonStyle} {grayStyle} w-full"
                    on:click={() => {
                        isOpen = false;
                    }}
                >
                    Cancel
                </button>
            </div>
        </div>
    </div>
{/if}