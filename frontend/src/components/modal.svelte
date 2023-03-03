<script>
    import { goto } from '$app/navigation';
    export let status, message, dest;
    console.log(status, message, dest);
</script>

{#if message}
    {#if status === 0}
        <!--Error popup-->
        <div class="z-50 fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="error-popup">
            <div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
                <div class="mt-3 text-center">
                    <div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-red-100">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-14 h-14 text-red-600">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                        </svg>                 
                    </div>

                    <h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">
                        Error
                    </h3>
                    <div class="px-7">
                        <p class="text-sm text-gray-500">
                            {message}
                        </p>
                    </div>
            
                    <div class="mr-2 ml-2 flex items-center px-4 py-3">
                        <button 
                            id="ok-btn"
                            on:click={() => {
                                message = null;
                            }}
                            class="px-4 py-2 border border-red-600 text-red-600 text-base font-medium rounded-md w-full shadow-sm bg-red-100 hover:border-red-800 hover:bg-red-400 focus:outline-none focus:ring-2 focus:ring-red-400"
                        >
                            OK
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {:else}
        <!-- Success popup + route -->
        <div class="z-50 fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="success-popup">
            <div class="relative top-60 mx-auto p-3 border w-80 shadow-lg rounded-lg bg-white border-gray-700">
                <div class="mt-3 text-center">
                    <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-green-600">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                        </svg>                     
                    </div>
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mt-2">Success!</h3>
                    <div class="px-7">
                        <p class="text-sm text-gray-500">
                            {message}
                        </p>
                    </div>
            
                    <div class="mr-2 ml-2 flex items-center px-4 py-3">
                        <button 
                            id="continue-btn" 
                            on:click={() => {
                                if (dest) goto(dest);
                                message = null;
                            }}
                            class="px-4 py-2 border border-green-600 text-green-600 text-base font-medium rounded-md w-full shadow-sm bg-green-100 hover:border-green-800 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400"
                        >
                            OK
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {/if}
{/if}