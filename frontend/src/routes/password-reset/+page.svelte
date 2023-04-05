<script>
	import { completePasswordReset, initiatePasswordReset } from "../../../requests/account";
	import ForgotPassword from "./forgotPassword.svelte";
	import ResetPassword from "./resetPassword.svelte";
	import { pushPopup } from "../../stores";

    let form = {
        'phone': '',
        'newPassword': '',
        'otp': '',
        'confirmPassword': ''
    }
    let errorMessage;
    let successPopup;

    let page = 1;

    const _initiatePasswordReset = async () => {
        const formattedPhone = '+1' + form.phone.replace(/\D/g, '');
        console.log(formattedPhone)
        if (formattedPhone.toString().length !== 12) {
            pushPopup(0, 'The phone number you input is not the correct length or incorrectly formatted. Please try again.');
            return;
        }

        const success = await initiatePasswordReset(formattedPhone);
        if (!success) {
            return;
        }

        form.phone = formattedPhone;
        page++;
	};

    const _completePasswordReset = async () => {
        if (form.password !== form.confirmPassword) {
            errorMessage = 'Your inputs do not match. Please try again.';
            return;
        }
        
        const success = await completePasswordReset(form.phone, form.otp, form.password);
	};
</script>

{#if page == 1}
    <ForgotPassword
        form={form}
        _submit={_initiatePasswordReset}
    />
{:else}
    <ResetPassword
        form={form}
        _submit={_completePasswordReset}
    />
{/if}