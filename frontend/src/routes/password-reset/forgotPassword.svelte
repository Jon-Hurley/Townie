<script>
    export let form, _submit;
</script>

<div class="fixed inset-0 bg-gray-100 overflow-y-auto h-full w-full">
    <div class="relative top-60 mx-auto p-3 w-80 shadow-lg rounded-lg border bg-white">
        <div class="mt-3 text-left">
            <div class="px-7">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                    Enter phone number
                </h3>
                <p class="mt-3 text-sm text-gray-500">
                    Please enter the phone number linked to your account. Do not include any special characters.
                </p>
            </div>

            <div class="mt-2 mr-2 ml-2 flex items-center px-4 py-3">
                <label for="username" class="sr-only">
                    Phone Number
                </label>
                <input
                    placeholder="Phone number"
                    bind:value={form.phone}
                    class="relative block w-full appearance-none rounded-b-md rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                >
            </div>
        </div>
        <div class="mt-2 mx-6 mb-3 grid grid-cols-2 gap-4 flex items-end">
            <div>
                <button
                    on:click={_submit}
                    name=submit
                    class="group relative w-full text-center items-end rounded-md border border-gray-600 py-2 px-4 text-md font-medium text-gray-600 hover:text-gray-800 focus:outline-gray-600"
                >
                    Submit
                </button> 
            </div>
            <div>
                <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-400">
                <button
                    name=cancel
                    class="group relative w-full text-center items-end rounded-md border border-red-600 py-2 px-4 text-md font-medium text-red-600 hover:text-red-800 focus:outline-red-600"
                >
                    Cancel
                </button> 
                </a>
            </div>
        </div>
    </div>
</div>