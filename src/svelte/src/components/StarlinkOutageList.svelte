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
<div style="display:flex; flex-flow:column; align-items: center">
    <table>

        <tr><th style="text-align: left;"><span style="text-align: center;">Time</span></th>
            <th style="text-align: center;"><span>Cause</span>
            <th style="text-align: center;"><span>Duration (s)</span></th></tr>
    {#each outages as outage}
        <tr>
            <td style="text-align: left;"><span>{new Date((outage.start_timestamp / 1000000) + 315964817000).toLocaleString()}</span></td>
            <td style="text-align: center;"><span>{outage.cause}</span></td>
            <td style="text-align: center;"><span>{outage.duration.toFixed(2)}</span></td>
        </tr>
    {/each}
    </table>
</div>
