<script>
    import {
        extent,
        scaleLinear,
        line,
        curveBasis
    } from "d3";

    import Axis from "./Axis.svelte";

    export let XAxisTitle = "";
    export let YAxisTitle = "";
    export let dataset = [];
    export let width = 900,
        height = 600,
        barWidth = 40;
    const margin = { top: 15, bottom: 50, left: 50, right: 20 };

    const innerHeight = height - margin.top - margin.bottom,
        innerWidth = width - margin.left - margin.right;

    $: xScale = scaleLinear()
        .domain([0, dataset.length])
        .range([0, innerWidth])
        .nice();

    $: yScale = scaleLinear()
        .domain(extent(dataset, (d) => d.y))
        .range([innerHeight, 0])
        .nice();
</script>

<main>
    <svg {width} {height}>
        <g class="lineChart" transform={`translate(${margin.left},${margin.top})`}>
            <Axis {innerHeight} {margin} scale={xScale} position="bottom" numTicks={dataset.length - 1}
                  tickFormat={function(d) {if (d < dataset.length && Number.isInteger(d)) return dataset[d].x; else return null;}} />
            <Axis {innerHeight} {margin} scale={yScale} position="left" />
            <text transform={`translate(${-30},${innerHeight / 2}) rotate(-90)`}>{YAxisTitle}</text>
            {#each dataset as point, i}
                <rect
                    x = "{xScale(i) - (barWidth/2)}"
                    y = "{yScale(point.y)}"
                    width = "{barWidth - 4}"
                    height = "{yScale(0) - yScale(point.y)}"
                    fill="blue"></rect>
            {/each}
            <text x={innerWidth / 2} y={innerHeight + 35}>{XAxisTitle}</text>
        </g>
    </svg>
</main>

<style>
    path {
        fill: transparent;
        stroke: rgb(18, 153, 90);
        stroke-width: 2.5;
        stroke-linejoin: round;
    }
</style>
