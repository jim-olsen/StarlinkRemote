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

    let dashboard = true;
    let outages = false;
    let allComponents = false;
</script>

<div style="display:flex; flex-flow:row">
    <button class="tabButton" on:click={()=> {dashboard=true; outages=false;allComponents=false;}}>Dashboard</button>
    <button class="tabButton" on:click={()=> {dashboard=false; outages=true; allComponents=false;}}
    <button class="tabButton" on:click={()=> {dashboard=false; outages=false;allComponents=true;}}>All Components</button>
</div>
<StarlinkDataFetcher/>

{#if dashboard}
    <div style="display:flex; flex-flow:column; justify-content: flex-start">
        <div style="display:flex; flex-flow: row; justify-content: space-around;">
            <StarlinkStatusIndicator/>
            <div style="display:flex; flex-flow: row; justify-content: space-between; gap: 50px">
                <div style="display:flex; justify-content: flex-start; flex-flow: column; align-items: center">
                    <span><b>Alerts</b></span>
                    <hr style="width: 100%"/>
                    <StarlinkAlerts/>
                </div>
                <div style="display:flex; justify-content: flex-start; flex-flow: column; align-items: center; gap: 10px">
                    <span><b>Obstruction Map</b></span>
                    <StarlinkObstructionMap width=200 height=200 />
                </div>
            </div>
        </div>
        <div style="display:flex; flex-flow: row; justify-content: space-evenly; gap: 20px;">
            <div style="display:flex; flex-flow: column; justify-content: flex-start;">
                <span><b>Upload Speed</b></span>
                <hr style="width: 100%"/>
                <StarlinkUploadDataRates chartWidth=600 chartHeight=200/>
            </div>
            <div style="display:flex; flex-flow: column; justify-content: flex-start;">
                <span><b>Download Speed</b></span>
                <hr style="width: 100%"/>
                <StarlinkDownloadDataRates chartWidth=600 chartHeight=200/>
            </div>
        </div>
        <div style="display:flex; flex-flow: row; justify-content: space-evenly; gap: 20px;">
            <div style="display:flex; flex-flow: column; justify-content: flex-start;">
                <span><b>Ping Latency</b></span>
                <hr style="width: 100%"/>
                <StarlinkPingLatency chartWidth=600 chartHeight=200/>
            </div>
            <div style="display:flex; flex-flow: column; justify-content: flex-start;">
                <span><b>Ping Drop</b></span>
                <hr style="width: 100%"/>
                <StarlinkPingDrop chartWidth=600 chartHeight=200/>
            </div>
        </div>
    </div>
{/if}

{#if outages}
    <div style="display:flex; flex-flow: column; justify-content: flex-start">

    </div>
{/if}

{#if allComponents}
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
                <StarlinkUploadDataRates chartWidth=600 chartHeight=200/>
            </div>
            <div style="border: 1px solid white">
                <StarlinkDownloadDataRates chartWidth=600 chartHeight=200/>
            </div>
        </div>
        <div style="display:flex; flex-flow:row; justify-content: space-around">
            <div style="border: 1px solid white">
                <StarlinkPingLatency chartWidth=600 chartHeight=200/>
            </div>
            <div style="border: 1px solid white">
                <StarlinkPingDrop chartWidth=600 chartHeight=200/>
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
{/if}