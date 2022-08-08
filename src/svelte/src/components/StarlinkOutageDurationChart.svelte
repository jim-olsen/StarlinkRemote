<script>
    import { onDestroy } from 'svelte';
    import BarChart from "./d3/BarChart.svelte";
    import {starlinkHistory} from "../stores";

    let outageDurationChartData = [];


    const unsubscribeHistory = starlinkHistory.subscribe(history => {
        if (history.hasOwnProperty("outages")) {
                outageDurationChartData = [];
                let outagesByType = [];
                outagesByType[' '] = 0.0;
                history.outages.forEach(outage => {
                    if (!outagesByType.hasOwnProperty(outage.cause)) {
                        outagesByType[outage.cause] = 0.0;
                    }
                    outagesByType[outage.cause]+= outage.duration;
                });
                for (const type in outagesByType) {
                    if (outagesByType.hasOwnProperty(type)) {
                        outageDurationChartData.push({"x": type, "y": outagesByType[type]})
                    }
                }
            }});

    onDestroy(unsubscribeHistory);
</script>
<div class="center" style="display:flex; flex-flow:column; justify-content: center; align-items: center">
    <BarChart XAxisTitle="Outage Type" YAxisTitle="Duration (s)" dataset={outageDurationChartData} width=1200 height=300 />
</div>
