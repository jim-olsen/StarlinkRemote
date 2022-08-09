<script>
    let safety = true;

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
        <button on:click={() => doStow()} disabled="{safety}">Stow Dish</button>
        <button on:click={() => doUnstow()} disabled="{safety}">Unstow Dish</button>
        <button on:click={() => doReboot()} disabled="{safety}">Reboot Dish</button>
        <input id="safety" type="checkbox" bind:checked={safety}><label for="safety">Enable Controls</label>
    </div>
</div>