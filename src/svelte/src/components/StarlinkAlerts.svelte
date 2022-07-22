<script>
    import { onDestroy } from 'svelte';
    import { starlinkStatus } from "../stores";
    let alerts = [];

    const unsubscribeStatus = starlinkStatus.subscribe(status => {
        alerts = [];
        for (const property in status.alerts) {
            if (status.alerts.hasOwnProperty(property)) {
                alerts.push({alertName: property, alertState: status.alerts[property]})
            }
        }
    } );

    onDestroy(unsubscribeStatus)
</script>
<div style="display:flex; flex-flow: column;" >
    {#each alerts as alert}
        <div style="display:flex; flex-flow: row; justify-content: space-between; align-items: center; gap:10px;">
            <span>{alert.alertName}</span>
            {#if alert.alertState}
                <div style="background-color: red; border-radius: 9999px; height: 10px; width: 10px"></div>
            {:else}
                <div style="background-color: green; border-radius: 9999px; height: 10px; width: 10px"></div>
            {/if}
        </div>
    {/each}
</div>