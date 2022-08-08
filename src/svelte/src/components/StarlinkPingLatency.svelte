<script>
    import {onDestroy} from 'svelte';
    import LineChart from "./d3/LineChart.svelte";
    import {starlinkHistory} from "../stores";

    export let chartWidth = 600;
    export let chartHeight = 300;

    let pingLatency = 0.0;
    let pingLatencyMax = 0.0;
    let pingLatencyMin = 0.0;
    let pingLatencyAvg = 0.0;
    let pingLatencyChartData = [];

    const unsubscribeHistory = starlinkHistory.subscribe(history => {
        if (history.hasOwnProperty("uplink_bps")) {
            pingLatencyChartData = [];
            history.ping_latency.forEach((value, i) => {
                pingLatencyChartData.unshift({"x": history.uplink_bps.length - i, "y": value});
            });
            pingLatencyMin = history.minimum_ping_latency.toFixed(2);
            pingLatencyMax = history.maximum_ping_latency.toFixed(2);
            pingLatencyAvg = history.average_ping_latency.toFixed(2);
            pingLatency = history.ping_latency[0].toFixed(2);
        }
    });

    onDestroy(unsubscribeHistory);
</script>
<div style="display:flex; flex-flow:row;gap: 10px;">
    <LineChart XAxisTitle="Elapsed Seconds" YAxisTitle="Latency (ms)" dataset={pingLatencyChartData} width={chartWidth}
               height={chartHeight}/>
    <div style="display:flex; flex-flow:column; justify-content: flex-start">
        <span><b>Cur: {pingLatency}</b></span>
        <span><b>Avg: {pingLatencyAvg}</b></span>
        <span><b>Min: {pingLatencyMin}</b></span>
        <span><b>Max: {pingLatencyMax}</b></span>
    </div>
</div>
