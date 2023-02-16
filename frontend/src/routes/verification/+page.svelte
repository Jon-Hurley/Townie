<script>
	import { goto } from '$app/navigation';
	import { PUBLIC_BACKEND_API } from '$env/static/public';
    import axios from 'axios';

    let remember;
	const form = {
		username: '',
		password: '',
        phoneNumber: ''
	};

    const signup = async () => {
        const res = await axios.post(
            PUBLIC_BACKEND_API + 'user/verification/'
        );
        console.log(res);
	};
</script>

<div class="text-sm text-center">
    <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
        Back to login
    </a>
</div>