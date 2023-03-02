<script>
    import { goto } from '$app/navigation';
	import { updateAccount, deleteUser } from "../../../requests/account";
    import { userStore } from "../../../stores";
   

    const title = "text-gray-700 font-semibold text-lg mt-6";
    const hr = "my-2 bg-gray-100 h-[2px]";

	let newUsername = '', newPhone = '';

    const _deleteUser = async () => {
        const res = await deleteUser($userStore.key);
		if (res) {
			goto('/login');
		}
        console.log(res);
	};


    const update = async () => {
        if (newUsername == '') {
            newUsername = $userStore.username;
        }
        if (newPhone == '') {
            newPhone = $userStore.phone;
        }
        
        const res = await updateAccount(newUsername, newPhone);
		if (res) {
			goto('/account/');
		}
        console.log(res);
	};
</script>

<div class="my-5 w-full">
    <div class="text-gray-700 font-bold text-3xl text-center">
        {$userStore.username}
    </div>
    <div class="text-gray-700 text-md text-center">
        #{$userStore.key}
    </div>
</div>

  
<div class="max-[200px]: grid grid-cols-8 gap-0 flex items-end">
<div class="col-span-2">
<div class={title}>
    <div class="text-align-top">
        Username
    </div>
</div>
</div>


<div class="col-start-5 col-span-4">
<!-- Delete User Function -->
<button
    on:click={_deleteUser}
    name=deleteAccount
    class="group relative w-full text-center items-end rounded-md border border-transparent py-2 px-4 text-md font-medium text-indigo-600 hover:text-indigo-800 focus:outline-none">

    <span class= "absolute bottom-2 right-2 flex pl-4">
        <!-- Heroicon name: trash can -->
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>          
    </span>
    Delete Account
</button>
    </div>
</div>


<hr class={hr}>
<div class="px-2 py-4">
    {$userStore.username}
    <input
        bind:value={newUsername}
        type="text"					
        class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        placeholder="New Username"
    />
</div>

<div class={title}>
    Phone Number
</div>
<hr class={hr}>
<div class="px-2 py-4 uppercase">
    {$userStore.phone}
    <input
        bind:value={newPhone}
        type="text"					
        class="relative block w-full appearance-none rounded-t-md rounded-b-md mt-2 border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
        placeholder="New Phone Number"
    />
</div>


<div class="mt-8 mr-2 ml-2 grid grid-cols-2 gap-4 flex items-end">
    <div>
        <button
            on:click={update}
            name=save
            class="group relative w-full text-center items-end rounded-md border border-indigo-400 py-2 px-4 text-md font-medium text-indigo-600 hover:text-indigo-800 focus:outline-none">
            Save Changes
        </button>
    </div>
    <div> 
        <a href="/account">
            <button
                name=cancel
                class="group relative w-full text-center items-end rounded-md border border-red-600 py-2 px-4 text-md font-medium text-red-600 hover:text-red-800 focus:outline-red">
                Cancel
            </button> 
        </a>
    </div>
</div>
  