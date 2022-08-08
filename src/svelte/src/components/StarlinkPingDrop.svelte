<script>
    import {onDestroy} from 'svelte';
    import LineChart from "./d3/LineChart.svelte";
    import {starlinkHistory} from "../stores";

    export let chartWidth = 600;
    export let chartHeight = 300;

    let pingDrop = 0.0;
    let pingDropMax = 0.0;
    let pingDropAvg = 0.0;
    let pingDropChartData = [];

    const unsubscribeHistory = starlinkHistory.subscribe(history => {
        if (history.hasOwnProperty("ping_drop_rate")) {
            pingDropChartData = [];
            history.ping_drop_rate.forEach((value, i) => {
                pingDropChartData.unshift({"x": history.ping_drop_rate.length - i, "y": (1 - value) * 100});
            });
            pingDropMax = (history.maximum_ping_drop_rate * 100).toFixed(2);
            pingDropAvg = (history.average_ping_drop_rate * 100).toFixed(2);
            pingDrop = (history.ping_drop_rate[0] * 100).toFixed(2);
        }
    });

    onDestroy(unsubscribeHistory);
</script>
<div style="display:flex; flex-flow: row;gap: 10px;">
    <LineChart XAxisTitle="Elapsed Seconds" YAxisTitle="Ping Loss %" dataset={pingDropChartData} height={chartHeight}
               width={chartWidth}/>
    <div style="display:flex; flex-flow: column; justify-content: flex-start;">
        <span><b>Cur: {pingDrop}%</b></span>
        <span><b>Avg: {pingDropAvg}%</b></span>
        <span><b>Max: {pingDropMax}%</b></span>
    </div>
</div>
