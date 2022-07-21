<script>
    import StarlinkRawData from "./components/StarlinkRawData.svelte"
    import StarlinkObstructionMap from "./components/StarlinkObstructionMap.svelte";
    import StarlinkUploadDataRates from "./components/StarlinkUploadDataRates.svelte"
    import StarlinkDownloadDataRates from "./components/StarlinkDownloadDataRates.svelte"
    import StarlinkDataFetcher from "./components/StarlinkDataFetcher.svelte";
</script>

<StarlinkDataFetcher/>
<div style="border: 1px solid black">
    <StarlinkRawData/>
</div>
<div style="display: flex; flex-flow: column; justify-content: center">
    <div style="border: 1px solid black">
        <StarlinkObstructionMap/>
    </div>
    <div style="display:flex; flex-flow:row; justify-content: space-around">
        <div style="border: 1px solid black">
            <StarlinkUploadDataRates/>
        </div>
        <div style="border: 1px solid black">
            <StarlinkDownloadDataRates/>
        </div>
    </div>
</div>