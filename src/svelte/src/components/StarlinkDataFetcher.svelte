<script>
    import {starlinkStatus} from "../stores";
    import {starlinkHistory} from "../stores";

    function getStatus() {
        fetch("/starlink/status/", {
            headers: {
                "Accept": "application/json"
            }
        })
            .then(d => d.json())
            .then(d => {
                $starlinkStatus = d
            });
    }

    function getHistory() {
        fetch("/starlink/history/", {
            headers: {
                "Accept": "application/json"
            }
        })
            .then(d => d.json())
            .then(d => {
                $starlinkHistory = d
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
        historyInterval = setInterval(getHistory, 1000)
    }

</script>