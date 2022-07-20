<script>
    import StarlinkRawData from "./components/StarlinkRawData.svelte"
    import StarlinkObstructionMap from "./components/StarlinkObstructionMap.svelte";
    import StarlinkDataRates from "./components/StarlinkDataRates.svelte"
</script>

<StarlinkRawData/>
<div style="display: flex; flex-flow: column; justify-content: center">
    <StarlinkObstructionMap/>
    <StarlinkDataRates/>
</div>