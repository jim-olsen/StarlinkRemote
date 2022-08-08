<script>
    import {onMount} from 'svelte';
    import * as d3 from 'd3';

    export let value = 0;
    $: {
        update(value)
    }

    export let size = 300;
    export let clipWidth = size;
    export let clipHeight = size;
    export let ringInset = 20;
    export let ringWidth = 60;
    export let pointerWidth = 10;
    export let pointerTailLength = 5;
    export let pointerHeadLengthPercent = 0.9;
    export let minValue = 0;
    export let maxValue = 360;
    export let minAngle = 0;
    export let maxAngle = 360;
    export let transitionMs = 4000;
    export let majorTicks = 20;
    export let labelFormat = d3.format(',d');
    export let labelInset = 15;
    export let arcColorFn = d3.interpolateHsl(d3.rgb('#e8e2ca'), d3.rgb('#3e6c0a'))
    let that = {};
    let range = undefined;
    let r = undefined;
    let pointerHeadLength = undefined;

    let svg = undefined;
    let arc = undefined;
    let scale = undefined;
    let ticks = undefined;
    let tickData = undefined;
    let pointer = undefined;
    let isRendered = false;

    let donut = d3.pie();

    function deg2rad(deg) {
        return deg * Math.PI / 180;
    }

    function newAngle(d) {
        var ratio = scale(d);
        var newAngle = minAngle + (ratio * range);
        return newAngle;
    }

    function configure() {
        range = maxAngle - minAngle;
        r = size / 2;
        pointerHeadLength = Math.round(r * pointerHeadLengthPercent);

        // a linear scale that maps domain values to a percent from 0..1
        scale = d3.scaleLinear()
            .range([0, 1])
            .domain([minValue, maxValue]);

        ticks = scale.ticks(majorTicks);
        tickData = d3.range(majorTicks).map(function () {
            return 1 / majorTicks;
        });

        arc = d3.arc()
            .innerRadius(r - ringWidth - ringInset)
            .outerRadius(r - ringInset)
            .startAngle(function (d, i) {
                var ratio = d * i;
                return deg2rad(minAngle + (ratio * range));
            })
            .endAngle(function (d, i) {
                var ratio = d * (i + 1);
                return deg2rad(minAngle + (ratio * range));
            });
    }

    function centerTranslation() {
        return 'translate(' + r + ',' + r + ')';
    }

    function render(newValue) {
        svg = d3.select('#gauge')
            .append('svg:svg')
            .attr('class', 'gauge')
            .attr('width', clipWidth)
            .attr('height', clipHeight);

        var centerTx = centerTranslation();

        var arcs = svg.append('g')
            .attr('class', 'arc')
            .attr('transform', centerTx);

        arcs.selectAll('path')
            .data(tickData)
            .enter().append('path')
            .attr('fill', function (d, i) {
                return arcColorFn(d * i);
            })
            .attr('d', arc);

        var lg = svg.append('g')
            .attr('class', 'label')
            .attr('transform', centerTx);
        lg.selectAll('text')
            .data(ticks)
            .enter()
            .append('text')
            .attr('transform', (d, i) => {
                var ratio = scale(d);
                var newAngle = minAngle + (ratio * range);
                return 'rotate(' + newAngle + ') translate(0,' + (labelInset - r) + ')';
            })
            .text(labelFormat)
            .style('text-anchor', 'middle');

        var lineData = [[pointerWidth / 2, 0],
            [0, -pointerHeadLength],
            [-(pointerWidth / 2), 0],
            [0, pointerTailLength],
            [pointerWidth / 2, 0]];
        var pointerLine = d3.line();
        var pg = svg.append('g').data([lineData])
            .attr('class', 'pointer')
            .attr('transform', centerTx);

        pointer = pg.append('path')
            .attr('d', pointerLine/*function(d) { return pointerLine(d) +'Z';}*/)
            .attr('transform', 'rotate(' + minAngle + ')')
            .style('fill', '#FFFFFF');

        isRendered = true;
        update(newValue === undefined ? 0 : newValue);
    }

    function update(newValue) {
        if (isRendered) {
            var ratio = scale(newValue);
            var newAngle = minAngle + (ratio * range);
            pointer.transition()
                .duration(transitionMs)
                .attr('transform', 'rotate(' + newAngle + ')');
        }
    }

    onMount(() => {
        configure()
        render();
    })
</script>

<div id="gauge"></div>