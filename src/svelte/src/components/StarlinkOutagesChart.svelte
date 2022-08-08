<script>
    import { onDestroy } from 'svelte';
    import BarChart from "./d3/BarChart.svelte";
    import {starlinkHistory} from "../stores";

    let outagesChartData = [];

    const unsubscribeHistory = starlinkHistory.subscribe(history => {
        if (history.hasOwnProperty("outages_by_category")) {
                outagesChartData = [];
                outagesChartData.push({"x": " ", "y": 0})
                for (const outageType in history.outages_by_category) {
                    if (history.outages_by_category.hasOwnProperty(outageType)) {
                        outagesChartData.push({"x": outageType, "y": history.outages_by_category[outageType]})
                    }
                }
            }});

    onDestroy(unsubscribeHistory);
</script>
<div class="center" style="display:flex; flex-flow:column; justify-content: center; align-items: center">
    <BarChart XAxisTitle="Outage Type" YAxisTitle="Occurrences" dataset={outagesChartData} width=1200 height=300 />
</div>
