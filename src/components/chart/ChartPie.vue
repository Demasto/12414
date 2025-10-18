<script setup lang="ts">
import { ref } from 'vue'
import type {ImportsByYear} from "@/services/goods/GoodsAPI.ts";
const {dynamics = []} = defineProps<{
  dynamics: ImportsByYear[]
}>()

const options = ref({
  chart: {
    id: 'Круговая диаграмма - доля импорта на страну.'
  },
  labels: ['Apple', 'Mango', 'Orange', 'Watermelon', 'test'],
  colors: ['#667eea', '#3eba64', '#feb019', '#ff4560', '#008ffb', '#7f42e1']
})

const series = ref( [44, 55, 41, 17, 15])

function getImportShareByCountry(imports: ImportsByYear[], year: number = 2024) {
  // Фильтрация по году
  const itemsForYear = imports.filter(item => item.year === year);

  // Суммируем общий value_usd_mln
  const totalValue = itemsForYear.reduce((sum, item) => sum + item.value_usd_mln, 0);

  // Группируем по странам и суммируем value_usd_mln
  const grouped = itemsForYear.reduce((acc, item) => {
    acc[item.country] = (acc[item.country] || 0) + item.value_usd_mln;
    return acc;
  }, {} as Record<string, number>);

  // Сортируем страны по убыванию value_usd_mln
  const sorted = Object.entries(grouped)
      .sort((a, b) => b[1] - a[1]);

  // Получаем топ 5
  const top5 = sorted.slice(0, 5);

  // Сумма топ 5
  const top5Sum = top5.reduce((sum, [, val]) => sum + val, 0);

  // Остальные
  const othersValue = totalValue - top5Sum;

  // Формируем результат с процентами
  const result = top5.map(([country, val]) => ({
    country,
    percent: ((val / totalValue) * 100).toFixed(2)
  }));

  if (othersValue > 0) {
    result.push({
      country: "остальные",
      percent: ((othersValue / totalValue) * 100).toFixed(2),
      color: '#7f42e1'
    });
  }

  return result;
}

const importByCountry = getImportShareByCountry(dynamics)
options.value.labels = importByCountry.map((item) => item.country)
series.value = importByCountry.map((item) => Number(item.percent))
</script>


<template>
  <apexchart type="pie" :options="options" :series="series"/>
</template>

<style scoped>

</style>
