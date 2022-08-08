<script>
    import {onDestroy} from 'svelte';
    import {starlinkStatus} from "../stores";

    let uptime = "";

    const unsubscribeStatus = starlinkStatus.subscribe(status => {
        if (status.hasOwnProperty("uptime")) {
            var days = status["uptime"] / (3600*24),
                hours = (status["uptime"] / 3600 % 24),
                minutes = (hours % 1) * 60,
                seconds = (minutes % 1) * 60;
            uptime = Math.floor(days) + " days, " + Math.floor(hours) + " hours, " + Math.floor(minutes) + " minutes, " + Math.round(seconds) + " seconds";        }
    });

    onDestroy(unsubscribeStatus)
</script>
<div style="display:flex; flex-flow: column;justify-content: center;">
    <span><b>Uptime: {uptime}</b></span>
</div>
