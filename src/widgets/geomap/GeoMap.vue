<template>
  <div>
    <h2>Мировая карта импорта по товару</h2>
    <div class="zoom-info mb_10">
      Текущий зум: {{ zoomLevel }}
    </div>
    <div class="border-card">
      <div ref="tooltipRef" class="tooltip" style="display:none"></div>
      <svg ref="svgRef" width="100%" height="100%" style="height: 80vh;" @zoom.stop @resize.stop @scroll.stop></svg>
    </div>
  </div>
</template>


<script setup lang="ts">
import * as d3 from "d3";
import { onMounted, ref } from "vue";
import type {ImportsByYear} from "@/services/goods/GoodsAPI.ts";

const svgRef = ref<SVGSVGElement | null>(null);
const tooltipRef = ref<HTMLDivElement | null>(null);
const zoomLevel = ref('1.00');

const {dict = {}} = defineProps<{
  dict: Record<string, ImportsByYear>;
}>()

function makeTooltip(name: string) {
  const {value_tons = 'Нет данных', value_usd_mln = 'Нет данных', country_group = 'Нет данных'} = dict[name] || {};
  return `<strong>${name} - ${country_group}</strong><br><b>Импорт (Млн.$): ${value_usd_mln}</b>`
}


onMounted(async () => {

  svgRef.value?.addEventListener('wheel', (event) => {
    // предотвращаем прокрутку страницы
    event.preventDefault();
  }, { passive: false });

  const {clientHeight: height, clientWidth: width} = svgRef.value || {}
  // размеры карты
  // const width = window.innerWidth;
  // const height = window.innerHeight;


  const svg = d3.select(svgRef.value);
  const tooltip = d3.select(tooltipRef.value);

  const g = svg.append("g");

  // базовая проекция мира
  const projection = d3.geoMercator().scale(140).translate([width / 2, height / 1.5]);
  const path = d3.geoPath().projection(projection);

  // загружаем GeoJSON (например public/world.geojson)
  const geojson = await d3.json("/world.geojson");

  g.selectAll("path")
      .data((geojson as any).features)
      .enter()
      .append("path")
      .attr("d", path)
      .attr("fill", "rgba(127,66,225,0.38)")
      .attr("stroke", "#333")
      .attr("stroke-width", 0.2)
      .on("mouseover", function () {
        d3.select(this)
            .raise() // поднимаем над другими
            .transition()
            .duration(0)
            .attr("fill", "#7f42e1")
            .attr("stroke-width", 1);
      })
      .on("mousemove", function (event, d) {
        const name = d.properties?.shapeName || "—";
        tooltip
            .style("display", "block")
            .style("left", event.pageX + 10 + "px")
            .style("top", event.pageY + 10 + "px")
            .html(makeTooltip(name));
      })
      .on("mouseout", function () {
        tooltip.style("display", "none");

        d3.select(this)
            .transition()
            .duration(0)
            .attr("fill", "rgba(127,66,225,0.38)")
            .attr("stroke-width", 0.2);
      })
      .on("click", (event, d) => {
        const name = d.properties?.shapeName || "—";
        alert(`Клик по стране: ${name}`);
      });

  // === Добавляем ЗУМ ===
  const zoom = d3.zoom()
      .scaleExtent([1, 8]) // диапазон зума
      .on("zoom", (event) => {
        zoomLevel.value = event.transform.k.toFixed(2); // <–– отслеживаем текущий зум
        g.attr("transform", event.transform);
      });

  svg.call(zoom as any);

});
</script>

<style scoped>

svg {
  background-color: #f8f9fa;

}

.border-card {
  border: 0.2rem solid #7f42e1;
}


.tooltip {
  position: absolute;
  pointer-events: none;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 13px;
  z-index: 9999;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
</style>