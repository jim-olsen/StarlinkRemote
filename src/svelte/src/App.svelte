<script>
    import StarlinkRawData from "./components/StarlinkRawData.svelte"
    import StarlinkObstructionMap from "./components/StarlinkObstructionMap.svelte";
    import StarlinkUploadDataRates from "./components/StarlinkUploadDataRates.svelte"
    import StarlinkDownloadDataRates from "./components/StarlinkDownloadDataRates.svelte"
    import StarlinkDataFetcher from "./components/StarlinkDataFetcher.svelte";
    import StarlinkPingLatency from "./components/StarlinkPingLatency.svelte";
    import StarlinkPingDrop from "./components/StarlinkPingDrop.svelte"
</script>

<StarlinkDataFetcher/>
<div style="display: flex; flex-flow: column; justify-content: space-around">
    <div style="border: 1px solid white">
        <StarlinkRawData/>
    </div>
    <div style="border: 1px solid white">
        <StarlinkObstructionMap/>
    </div>
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid white">
            <StarlinkUploadDataRates/>
        </div>
        <div style="border: 1px solid white">
            <StarlinkDownloadDataRates/>
        </div>
    </div>
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid white">
            <StarlinkPingLatency/>
        </div>
        <div style="border: 1px solid white">
            <StarlinkPingDrop/>
        </div>
    </div>
</div>