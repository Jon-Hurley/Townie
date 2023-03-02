<script>
	import { get } from "svelte/store";
    import { userStore } from "../../stores";
</script>

<a href={`/user/${get(userStore).key}`}>
    View Profile
</a>