<script>
	import { purchaseStore } from "../../../requests/store";
</script>

<div>
    {#each $purchaseStore as p}
        <div>
            {p.name}
        </div>
    {/each}
</div>