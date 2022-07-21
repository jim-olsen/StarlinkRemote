<script>
    import { onDestroy } from 'svelte';
    import LineChart from "./d3/LineChart.svelte";
    import {starlinkHistory} from "../stores";

    let pingDrop = 0.0;
    let pingDropMax = 0.0;
    let pingDropAvg = 0.0;
    let pingDropChartData = [];

    const unsubscribeHistory = starlinkHistory.subscribe(history => {
        if (history.hasOwnProperty("ping_drop_rate")) {
                pingDropChartData = [];
                history.ping_drop_rate.forEach((value, i) =>  {
                    pingDropChartData.unshift({"x": history.ping_drop_rate.length - i, "y": (1 - value) * 100});
                });
                pingDropMax = (history.maximum_ping_drop_rate * 100).toFixed(2);
                pingDropAvg = (history.average_ping_drop_rate * 100).toFixed(2);
                pingDrop = (history.ping_drop_rate[history.ping_drop_rate.length - 1] * 100).toFixed(2);
            }});

    onDestroy(unsubscribeHistory);
</script>
<div class="center" style="display:flex; flex-flow:column; justify-content: center; align-items: baseline">
    <LineChart XAxisTitle="Time" YAxisTitle="Ping Loss %" dataset={pingDropChartData} width=600 height=300 />
    <h2>{pingDrop}% / {pingDropAvg}% / {pingDropMax}%</h2>
    <h4>Ping Drop (current/avg/max)</h4>
</div>
