<script>
    import { onDestroy } from 'svelte';
    import LineChart from "./d3/LineChart.svelte";
    import {starlinkHistory} from "../stores";

    let pingLatency = 0.0;
    let pingLatencyMax = 0.0;
    let pingLatencyMin = 0.0;
    let pingLatencyAvg = 0.0;
    let pingLatencyChartData = [];

    const unsubscribeHistory = starlinkHistory.subscribe(history => {
        if (history.hasOwnProperty("uplink_bps")) {
                pingLatencyChartData = [];
                history.ping_latency.forEach((value, i) =>  {
                    pingLatencyChartData.unshift({"x": history.uplink_bps.length - i, "y": value});
                });
                pingLatencyMin = history.minimum_ping_latency.toFixed(2);
                pingLatencyMax = history.maximum_ping_latency.toFixed(2);
                pingLatencyAvg = history.average_ping_latency.toFixed(2);
                pingLatency = history.ping_latency[history.ping_latency.length - 1].toFixed(2);
            }});

    onDestroy(unsubscribeHistory);
</script>
<div class="center" style="display:flex; flex-flow:column; justify-content: center; align-items: baseline">
    <LineChart XAxisTitle="Time" YAxisTitle="Latency (ms)" dataset={pingLatencyChartData} width=600 height=300 />
    <h2>{pingLatency} / {pingLatencyAvg} / {pingLatencyMin} / {pingLatencyMax}</h2>
    <h4>Ping Latency (current/avg/min/max) ms</h4>
</div>
