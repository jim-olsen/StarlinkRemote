<script>
    import {onDestroy} from 'svelte';
    import {starlinkStatus} from "../stores";

    let services = [];
    let state = "UNKNOWN";

    const unsubscribeStatus = starlinkStatus.subscribe(status => {
        state = status.state;
        services = [];
        for (const property in status.ready_states) {
            if (status.ready_states.hasOwnProperty(property)) {
                services.push({serviceName: property, serviceState: status.ready_states[property]})
            }
        }
        services.push({serviceName: "gps", serviceState: status["gps_valid"]})
        services.push({serviceName: "snr", serviceState: status["snr_above_noise_floor"]})
    });

    onDestroy(unsubscribeStatus)
</script>
<div style="display:flex; flex-flow:column">
    <div style="display:flex; flex-flow: row; justify-content: center; align-items: center; gap: 30px;">
        <h4>{state}</h4>
        {#if state == 'CONNECTED'}
            <div style="background-color: green; border-radius: 9999px; height: 30px; width: 30px"></div>
        {:else}
            <div style="background-color: red; border-radius: 9999px; height: 30px; width: 30px"></div>
        {/if}
    </div>
    <div style="display:flex; flex-flow: row; justify-content: space-around; gap: 20px;">
        {#each services as service}
            <div style="display:flex; flex-flow: row; justify-content: space-between; align-items: center; gap:10px;">
                <h4>{service.serviceName}</h4>
                {#if service.serviceState}
                    <div style="background-color: green; border-radius: 9999px; height: 10px; width: 10px"></div>
                {:else}
                    <div style="background-color: red; border-radius: 9999px; height: 10px; width: 10px"></div>
                {/if}
            </div>
        {/each}
    </div>
</div>