<script>
    import JSONTree from 'svelte-json-tree';

    let rawJson = {};

    function getStatus() {
        fetch("./starlink/status")
            .then(d => d.json())
            .then(d => rawJson = d);
    }
</script>

<JSONTree value="{rawJson}"/>
<button on:click={getStatus}>Get Dishy Status</button>