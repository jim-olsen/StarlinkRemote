<script>
    import LineChart from "./d3/LineChart.svelte";
    let uploadMbps = 0.0
    let downloadMbps = 0.0
    let uploadChartData = []
    let downloadChartData = []

    function getStatus() {
        fetch("./starlink/status")
            .then(d => d.json())
            .then(d => {
                uploadMbps = (d.uplink_throughput_bps / 1000000).toFixed(2)
                downloadMbps = (d.downlink_throughput_bps / 1000000).toFixed(2)
            });
    }

    function getHistory() {
        fetch("./starlink/history")
            .then(d => d.json())
            .then(d => {
                uploadChartData = []
                d.uplink_bps.forEach((value, i) =>  {
                    uploadChartData.unshift({"x": i, "y": value / 1000000})
                });
                downloadChartData = []
                d.downlink_bps.forEach((value, i) => {
                    downloadChartData.unshift({"x": i, "y": value / 1000000})
                });
            });
    }

    let statusInterval
    $: {
        clearInterval(statusInterval)
        statusInterval = setInterval(getStatus, 500)
    }
    let historyInterval
    $: {
        clearInterval(historyInterval)
        historyInterval = setInterval(getHistory, 500)
    }
</script>
<div style="display:flex; flex-flow:row; justify-content: space-around">
    <div class="center" style="display:flex; flex-flow:column; justify-content: center; align-items: baseline">
        <LineChart XAxisTitle="Time" YAxisTitle="Upload MMps" dataset={uploadChartData}/>
        <h2>{uploadMbps}</h2>
        <h4>Upload Mbps</h4>
    </div>
    <div style="display:flex; flex-flow:column; justify-content: center; align-items: baseline">
        <LineChart XAxisTitle="Time" YAxisTitle="Download MBps" dataset={downloadChartData}/>
        <h2>{downloadMbps}</h2>
        <h4>Download MBps</h4>
    </div>
</div>