<template>
  <div>
    <h2>Мировая карта импорта по товару</h2>
    <div class="zoom-info mb_10">Текущий зум: {{ zoomLevel }}</div>

    <div class="border-card">
      <div ref="tooltipRef" class="tooltip" style="display:none"></div>
      <svg ref="svgRef" width="100%" height="100%" style="height: 80vh;" @zoom.stop @resize.stop @scroll.stop></svg>
    </div>

    <!-- Легенда -->
    <div class="legend">
      <span class="legend-item">
        <i class="legend-chip friendly"></i> Дружественная страна
      </span>
      <span class="legend-item">
        <i class="legend-chip unfriendly"></i> Недружественная страна
      </span>
      <span class="legend-item">
        <i class="legend-chip unknown"></i> Нет данных
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import * as d3 from "d3";
import { onMounted, ref } from "vue";
import type { ImportsByYear } from "@/services/goods/GoodsAPI.ts";

const svgRef = ref<SVGSVGElement | null>(null);
const tooltipRef = ref<HTMLDivElement | null>(null);
const zoomLevel = ref("1.00");

const { dict = {} } = defineProps<{
  dict: Record<string, ImportsByYear>;
}>();

/** Нормализация названий (shapeName -> ключ словаря) */
function norm(s?: string): string {
  return (s || "").trim().toLowerCase()
      .replace(/[\u2010-\u2015]/g, "-")       // разные тире
      .replace(/\s+/g, " ")
      .replace(/^the\s+/i, "");               // The Bahamas -> Bahamas
}

/** Получаем запись по стране с fallback-ами */
function getRecByCountryName(name: string): ImportsByYear | undefined {
  // основные варианты
  const key = norm(name);
  // прямое совпадение
  for (const k of Object.keys(dict)) {
    if (norm(k) === key) return dict[k];
  }
  // частичные трюки (пример: Russian Federation vs Russia)
  const alt = key
      .replace(/federation|republic|people'?s|democratic|kingdom/g, "")
      .replace(/\s{2,}/g, " ")
      .trim();
  if (alt && alt !== key) {
    for (const k of Object.keys(dict)) {
      if (norm(k) === alt) return dict[k];
    }
  }
  return undefined;
}

type Group = "friendly" | "unfriendly" | "unknown";
function getGroup(rec?: ImportsByYear): Group {
  if (!rec) return "unknown";
  const v = (rec.country_group || "").toLowerCase();
  if (v === "unfriendly") return "unfriendly";
  if (v === "friendly") return "friendly";
  return "unknown";
}

function groupLabelRu(g: Group): string {
  if (g === "unfriendly") return "Недружественная страна";
  if (g === "friendly") return "Дружественная страна";
  return "нет данных";
}

function fmtMln(x: any): string {
  const n = Number(x);
  if (!isFinite(n)) return "Нет данных";
  return n.toLocaleString("ru-RU", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function makeTooltip(name: string) {
  const rec = getRecByCountryName(name);
  const grp = getGroup(rec);
  const label = groupLabelRu(grp);
  const usd = rec?.value_usd_mln ?? NaN;
  return `<strong>${name} — ${label}</strong><br><b>Импорт (млн $): ${fmtMln(usd)}</b>`;
}

/** Цвета заливки */
function fillByGroup(g: Group): string {
  switch (g) {
    case "friendly":   return "rgba(36, 156, 72, 0.55)";  // зелёный
    case "unfriendly": return "rgba(220, 53, 69, 0.55)";  // красный
    default:           return "rgba(108, 117, 125, 0.35)"; // серый
  }
}
/** Цвет при ховере (чуть насыщеннее) */
function fillHoverByGroup(g: Group): string {
  switch (g) {
    case "friendly":   return "rgba(36, 156, 72, 0.85)";
    case "unfriendly": return "rgba(220, 53, 69, 0.85)";
    default:           return "rgba(108, 117, 125, 0.6)";
  }
}

onMounted(async () => {
  svgRef.value?.addEventListener(
      "wheel",
      (event) => {
        event.preventDefault();
      },
      { passive: false }
  );

  // размеры
  const { clientHeight: height = 800, clientWidth: width = 1200 } = svgRef.value || {};

  const svg = d3.select(svgRef.value);
  const tooltip = d3.select(tooltipRef.value);
  const g = svg.append("g");

  // базовая проекция мира
  const projection = d3.geoMercator().scale(140).translate([width / 2, height / 1.5]);
  const path = d3.geoPath().projection(projection);

  // загружаем GeoJSON (public/world.geojson)
  const geojson = (await d3.json("/world.geojson")) as any;

  // отрисовка слоёв
  g.selectAll("path")
      .data(geojson.features)
      .enter()
      .append("path")
      .attr("d", path as any)
      .attr("fill", (d: any) => {
        const name = d.properties?.shapeName || "—";
        const rec = getRecByCountryName(name);
        const grp = getGroup(rec);
        return fillByGroup(grp);
      })
      .attr("stroke", "#333")
      .attr("stroke-width", 0.2)
      .on("mouseover", function (_event: any, d: any) {
        const name = d.properties?.shapeName || "—";
        const rec = getRecByCountryName(name);
        const grp = getGroup(rec);
        d3.select(this)
            .raise()
            .transition()
            .duration(120)
            .attr("fill", fillHoverByGroup(grp))
            .attr("stroke-width", 1);
      })
      .on("mousemove", function (event: any, d: any) {
        const name = d.properties?.shapeName || "—";
        tooltip
            .style("display", "block")
            .style("left", event.pageX + 10 + "px")
            .style("top", event.pageY + 10 + "px")
            .html(makeTooltip(name));
      })
      .on("mouseout", function (_event: any, d: any) {
        const name = d.properties?.shapeName || "—";
        const rec = getRecByCountryName(name);
        const grp = getGroup(rec);
        tooltip.style("display", "none");
        d3.select(this)
            .transition()
            .duration(120)
            .attr("fill", fillByGroup(grp))
            .attr("stroke-width", 0.2);
      })
      .on("click", (_event: any, d: any) => {
        const name = d.properties?.shapeName || "—";
        alert(`Клик по стране: ${name}`);
      });

  // ЗУМ
  const zoom = d3
      .zoom()
      .scaleExtent([1, 8])
      .on("zoom", (event: any) => {
        zoomLevel.value = event.transform.k.toFixed(2);
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
.legend {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 8px 0 0;
  font-size: 14px;
  color: #343a40;
}
.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.legend-chip {
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 3px;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,.25);
}
.legend-chip.friendly   { background: rgba(36,156,72,.75); }
.legend-chip.unfriendly { background: rgba(220,53,69,.75); }
.legend-chip.unknown    { background: rgba(108,117,125,.55); }
</style>

<!--<template>-->
<!--  <div>-->
<!--    <h2>Мировая карта импорта по товару</h2>-->
<!--    <div class="zoom-info mb_10">-->
<!--      Текущий зум: {{ zoomLevel }}-->
<!--    </div>-->
<!--    <div class="border-card">-->
<!--      <div ref="tooltipRef" class="tooltip" style="display:none"></div>-->
<!--      <svg ref="svgRef" width="100%" height="100%" style="height: 80vh;" @zoom.stop @resize.stop @scroll.stop></svg>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->


<!--<script setup lang="ts">-->
<!--import * as d3 from "d3";-->
<!--import { onMounted, ref } from "vue";-->
<!--import type {ImportsByYear} from "@/services/goods/GoodsAPI.ts";-->

<!--const svgRef = ref<SVGSVGElement | null>(null);-->
<!--const tooltipRef = ref<HTMLDivElement | null>(null);-->
<!--const zoomLevel = ref('1.00');-->

<!--const {dict = {}} = defineProps<{-->
<!--  dict: Record<string, ImportsByYear>;-->
<!--}>()-->

<!--function makeTooltip(name: string) {-->
<!--  const {value_tons = 'Нет данных', value_usd_mln = 'Нет данных', country_group = 'Нет данных'} = dict[name] || {};-->
<!--  return `<strong>${name} - ${country_group}</strong><br><b>Импорт (Млн.$): ${value_usd_mln}</b>`-->
<!--}-->


<!--onMounted(async () => {-->

<!--  svgRef.value?.addEventListener('wheel', (event) => {-->
<!--    // предотвращаем прокрутку страницы-->
<!--    event.preventDefault();-->
<!--  }, { passive: false });-->

<!--  const {clientHeight: height, clientWidth: width} = svgRef.value || {}-->
<!--  // размеры карты-->
<!--  // const width = window.innerWidth;-->
<!--  // const height = window.innerHeight;-->


<!--  const svg = d3.select(svgRef.value);-->
<!--  const tooltip = d3.select(tooltipRef.value);-->

<!--  const g = svg.append("g");-->

<!--  // базовая проекция мира-->
<!--  const projection = d3.geoMercator().scale(140).translate([width / 2, height / 1.5]);-->
<!--  const path = d3.geoPath().projection(projection);-->

<!--  // загружаем GeoJSON (например public/world.geojson)-->
<!--  const geojson = await d3.json("/world.geojson");-->

<!--  g.selectAll("path")-->
<!--      .data((geojson as any).features)-->
<!--      .enter()-->
<!--      .append("path")-->
<!--      .attr("d", path)-->
<!--      .attr("fill", "rgba(127,66,225,0.38)")-->
<!--      .attr("stroke", "#333")-->
<!--      .attr("stroke-width", 0.2)-->
<!--      .on("mouseover", function () {-->
<!--        d3.select(this)-->
<!--            .raise() // поднимаем над другими-->
<!--            .transition()-->
<!--            .duration(0)-->
<!--            .attr("fill", "#7f42e1")-->
<!--            .attr("stroke-width", 1);-->
<!--      })-->
<!--      .on("mousemove", function (event, d) {-->
<!--        const name = d.properties?.shapeName || "—";-->
<!--        tooltip-->
<!--            .style("display", "block")-->
<!--            .style("left", event.pageX + 10 + "px")-->
<!--            .style("top", event.pageY + 10 + "px")-->
<!--            .html(makeTooltip(name));-->
<!--      })-->
<!--      .on("mouseout", function () {-->
<!--        tooltip.style("display", "none");-->

<!--        d3.select(this)-->
<!--            .transition()-->
<!--            .duration(0)-->
<!--            .attr("fill", "rgba(127,66,225,0.38)")-->
<!--            .attr("stroke-width", 0.2);-->
<!--      })-->
<!--      .on("click", (event, d) => {-->
<!--        const name = d.properties?.shapeName || "—";-->
<!--        alert(`Клик по стране: ${name}`);-->
<!--      });-->

<!--  // === Добавляем ЗУМ ===-->
<!--  const zoom = d3.zoom()-->
<!--      .scaleExtent([1, 8]) // диапазон зума-->
<!--      .on("zoom", (event) => {-->
<!--        zoomLevel.value = event.transform.k.toFixed(2); // <–– отслеживаем текущий зум-->
<!--        g.attr("transform", event.transform);-->
<!--      });-->

<!--  svg.call(zoom as any);-->

<!--});-->
<!--</script>-->

<!--<style scoped>-->

<!--svg {-->
<!--  background-color: #f8f9fa;-->

<!--}-->

<!--.border-card {-->
<!--  border: 0.2rem solid #7f42e1;-->
<!--}-->


<!--.tooltip {-->
<!--  position: absolute;-->
<!--  pointer-events: none;-->
<!--  background: white;-->
<!--  border: 1px solid #ccc;-->
<!--  border-radius: 4px;-->
<!--  padding: 4px 8px;-->
<!--  font-size: 13px;-->
<!--  z-index: 9999;-->
<!--  box-shadow: 0 2px 6px rgba(0,0,0,0.15);-->
<!--}-->
<!--</style>-->