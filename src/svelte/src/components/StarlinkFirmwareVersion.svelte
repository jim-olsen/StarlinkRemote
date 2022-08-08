<script>
    import {onDestroy} from 'svelte';
    import {starlinkStatus} from "../stores";

    let firmware = "UNKNOWN";

    const unsubscribeStatus = starlinkStatus.subscribe(status => {
        if (status.hasOwnProperty("software_version")) {
            firmware = status["software_version"];
        }
    });

    onDestroy(unsubscribeStatus)
</script>
<div style="display:flex; flex-flow: column;justify-content: center;">
    <span><b>Firwmare Version: {firmware}</b></span>
</div>
