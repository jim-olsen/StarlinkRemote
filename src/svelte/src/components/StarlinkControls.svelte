<script>
    function doStow() {
        fetch('/starlink/stow', {method: 'POST'})
    }

    function doUnstow() {
        fetch('/starlink/unstow', {method: 'POST'})
    }

    function doReboot() {
        fetch('/starlink/reboot', {method: 'POST'})
    }
</script>
<div style="display: flex; flex-flow: column; justify-content: center">
    <div style="display:flex; flex-flow: row; justify-content: flex-start;gap: 20px">
        <button on:click={doStow()}>Stow Dish</button>
        <button on:click={doUnstow()}>Unstow Dish</button>
        <button on:click={doReboot()}>Reboot Dish</button>
    </div>
</div>