<script>
    import StarlinkRawData from "./components/StarlinkRawData.svelte"
    import StarlinkObstructionMap from "./components/StarlinkObstructionMap.svelte";
    import StarlinkUploadDataRates from "./components/StarlinkUploadDataRates.svelte"
    import StarlinkDownloadDataRates from "./components/StarlinkDownloadDataRates.svelte"
    import StarlinkDataFetcher from "./components/StarlinkDataFetcher.svelte";
    import StarlinkPingLatency from "./components/StarlinkPingLatency.svelte";
    import StarlinkPingDrop from "./components/StarlinkPingDrop.svelte"
    import StarlinkStatusIndicator from "./components/StarlinkStatusIndicator.svelte"
    import StarlinkOutagesChart from "./components/StarlinkOutagesChart.svelte"
    import StarlinkOutagesList from "./components/StarlinkOutageList.svelte"
    import StarlinkAlerts from "./components/StarlinkAlerts.svelte";
    import StarlinkOutageDurationChart from "./components/StarlinkOutageDurationChart.svelte";
</script>

<StarlinkDataFetcher/>
<div style="display: flex; flex-flow: column; justify-content: space-around">
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid white">
            <StarlinkStatusIndicator/>
        </div>
        <div style="border: 1px solid white">
            <StarlinkAlerts/>
        </div>
    </div>
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid white">
            <StarlinkUploadDataRates chartWidth=600 chartHeight=200 />
        </div>
        <div style="border: 1px solid white">
            <StarlinkDownloadDataRates chartWidth=600 chartHeight=200 />
        </div>
    </div>
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid white">
            <StarlinkPingLatency chartWidth=600 chartHeight=200 />
        </div>
        <div style="border: 1px solid white">
            <StarlinkPingDrop chartWidth=600 chartHeight=200 />
        </div>
    </div>
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid white">
            <StarlinkOutagesChart/>
        </div>
    </div>
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid white">
            <StarlinkOutageDurationChart/>
        </div>
    </div>
    <div style="border: 1px solid white">
        <StarlinkOutagesList/>
    </div>
    <div style="border: 1px solid white">
        <StarlinkObstructionMap/>
    </div>
    <div style="border: 1px solid white">
        <StarlinkRawData/>
    </div>
</div>