<script>
	import { onMount } from "svelte";
    import { goto } from '$app/navigation';

    import Modal from "../../../../general-components/modal.svelte";

    let isSuccess;

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);
        isSuccess = urlParams.get('success');
    })
</script>

<Modal
    status={isSuccess}
    message={
        isSuccess ? 'You have successfully activated premium. You can now access all premium features.'
                  : 'Failed to activate premium. Please try again, or close this page.'
    }
    onOk={() => {
        goto('/app/account');
    }}
/>