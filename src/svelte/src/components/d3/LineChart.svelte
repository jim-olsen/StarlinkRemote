<script>
    import {
        extent,
        scaleLinear,
        line,
        curveNatural,
        curveBasis
    } from "d3";

    import Axis from "./Axis.svelte";

    export let XAxisTitle = "";
    export let YAxisTitle = "";
    export let dataset = [];
    export let width = 900,
        height = 600;

    const margin = { top: 15, bottom: 50, left: 50, right: 20 };

    const innerHeight = height - margin.top - margin.bottom,
        innerWidth = width - margin.left - margin.right;

    $: xScale = scaleLinear()
        .domain(extent(dataset, (d) => d.x))
        .range([0, innerWidth])
        .nice();

    $: yScale = scaleLinear()
        .domain(extent(dataset, (d) => d.y))
        .range([innerHeight, 0])
        .nice();

    $: line_gen = line()
        .curve(curveBasis)
        .x((d) => xScale(d.x))
        .y((d) => yScale(d.y))(dataset);
</script>

<main>
    <svg {width} {height}>
        <g class="lineChart" transform={`translate(${margin.left},${margin.top})`}>
            <Axis {innerHeight} {margin} scale={xScale} position="bottom" />
            <Axis {innerHeight} {margin} scale={yScale} position="left" />
            <text transform={`translate(${-30},${innerHeight / 2}) rotate(-90)`}
            >{YAxisTitle}</text
            >
            <path d={line_gen} />
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
