<script>
    import JSONTree from 'svelte-json-tree';

    let rawJson = {};

    function getStatus() {
        fetch("./starlink/status/")
            .then(d => d.json())
            .then(d => rawJson = d);
    }

    function getHistory() {
        fetch("./starlink/history/")
            .then(d => d.json())
            .then(d => rawJson = d);
    }
</script>

<div>
    <JSONTree value="{rawJson}" defaultExpandedLevel="3"/>
    <button on:click={getStatus}>Get Dishy Status</button>
    <button on:click={getHistory}>Get Dishy History</button>
</div>
