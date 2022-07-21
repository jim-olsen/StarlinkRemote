<script>
    import { onDestroy } from 'svelte';
    import {starlinkHistory} from "../stores";

    let outages = []

    const unsubscribeHistory = starlinkHistory.subscribe(history => {
        if (history.hasOwnProperty("outages")) {
            outages = history.outages;
        }});

    onDestroy(unsubscribeHistory);
</script>
<div style="display:flex; flex-flow:column; align-items: flex-start">
    {#each outages as outage}
        <div style="display:flex; flex-flow: row; justify-content: space-between;gap: 10px;">
            <span>{outage.start_timestamp}</span>
            <span>{outage.cause}</span>
            <span>{outage.duration.toFixed(2)}</span>
        </div>
    {/each}
</div>
