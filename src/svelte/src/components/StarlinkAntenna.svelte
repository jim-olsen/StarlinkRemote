<script>
    import Guage from './d3/Gauge.svelte'
    import {starlinkStatus} from "../stores";
    import {onDestroy} from "svelte";

    let elevation = 0.0;
    let azimuth = 0.0;

    const unsubscribeStatus = starlinkStatus.subscribe(status => {
        if (status.hasOwnProperty("boresight_elevation")) {
            elevation = status["boresight_elevation"];
        }
        if (status.hasOwnProperty("boresight_azimuth")) {
            azimuth = 360 - status["boresight_azimuth"];
        }
    });

    onDestroy(unsubscribeStatus)
</script>
<div style="display: flex; flex-flow: row; justify-content: flex-start">
    <Guage value="{azimuth}" />
    <Guage size="600" minValue="0" maxValue="90" minAngle="-90" maxAngle="0" majorTicks="10" clipWidth="300" clipHeight="300" value="{elevation}" transitionMs="0"/>
</div>