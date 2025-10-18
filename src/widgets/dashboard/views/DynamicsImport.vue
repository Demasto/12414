<script setup lang="ts">

import type {ByYear, ImportsByYear} from "@/services/goods/GoodsAPI.ts";
import {ref} from "vue";

const {dynamics = []} = defineProps<{
  dynamics: ImportsByYear[]
}>()


// Сначала собираем все уникальные года для сортировки и сохранения порядка
const years = Array.from(new Set(dynamics.map(i => i.year))).sort()
//
// function groupByCountry(imports: ImportsByYear[]): CountryData[] {
//
//   // Создаём промежуточную структуру: country -> (year -> value)
//   const countryMap = new Map<string, Map<number, number>>();
//
//   for (const item of imports) {
//     if (!countryMap.has(item.country)) {
//       countryMap.set(item.country, new Map());
//     }
//     countryMap.get(item.country)!.set(item.year, item.value_usd_mln);
//   }
//
//   // Формируем итоговый массив
//   const result: CountryData[] = [];
//
//   for (const [country, yearMap] of countryMap.entries()) {
//     const data = years.map(year => yearMap.get(year) ?? 0);
//     result.push({ name: country, data });
//   }
//
//   return result;
// }

/**
 * Возвращает массив по годам, где каждый элемент — сумма value_usd_mln всех стран за этот год.
 */
function sumValueByYear(imports: ImportsByYear[]): string[] {
  // Собираем уникальные года и сортируем
  // const years = Array.from(new Set(imports.map(i => i.year))).sort();

  // Создаём Map: год -> сумма value_usd_mln
  const sumMap = new Map<number, number>();

  for (const item of imports) {
    const prev = sumMap.get(item.year) ?? 0;
    sumMap.set(item.year, prev + item.value_usd_mln);
  }

  // Формируем массив сумм по годам в отсортированном порядке
  return years.map(year => sumMap.get(year)?.toFixed(2) ?? 0);
}


function getTop5SKCByCountry(imports: ImportsByYear[], year: number) {
  // Отфильтровать данные по году
  const itemsForYear = imports.filter(item => item.year === year);

  // Группировка по странам
  const grouped = itemsForYear.reduce((acc, item) => {
    if (!acc[item.country]) {
      acc[item.country] = { value_usd_mln: 0, value_tons: 0 };
    }
    acc[item.country].value_usd_mln += item.value_usd_mln;
    acc[item.country].value_tons += item.value_tons;
    return acc;
  }, {} as Record<string, { value_usd_mln: number; value_tons: number }>);

  // Вычисление СКЦ для каждой страны
  const skcArray = Object.entries(grouped)
      .map(([country, data]) => {
        if (data.value_tons === 0) return null; // исключаем деление на 0
        return {
          country,
          skc: (data.value_usd_mln * 1_000_000) / data.value_tons
        };
      })
      .filter(Boolean) as { country: string; skc: number }[];

  // Сортировка по убыванию и выбор ТОП 5
  return skcArray.sort((a, b) => b.skc - a.skc).slice(0, 5);
}



console.log(getTop5SKCByCountry(dynamics, 2024));

const options = ref({
  chart: {
    id: 'Импорт'
  },
  xaxis: {
    categories: years
  },
  colors: ['#667eea', '#3eba64', '#feb019', '#ff4560', '#008ffb', '#7f42e1']
})

const series = ref([
  {
    name: 'Объём импорта млн. $',
    data: sumValueByYear(dynamics)
  }
])
</script>

<template>
  <section class="card">
    <h3>Объём и динамика импорта</h3>
<!--    <chart-line :dynamics="dynamics" />-->

    <apexchart type="line" :options="options" :series="series"></apexchart>
  </section>
</template>

<style scoped>

</style>