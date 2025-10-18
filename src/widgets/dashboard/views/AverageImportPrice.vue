<script setup lang="ts">

import type {ImportsByYear} from "@/services/goods/GoodsAPI.ts";

const {dynamics = []} = defineProps<{
  dynamics: ImportsByYear[]
}>()


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
          skc: Number(((data.value_usd_mln * 1_000_000) / data.value_tons).toFixed(0)),
        };
      })
      .filter(Boolean) as { country: string; skc: number }[];

  // Сортировка по убыванию и выбор ТОП 5
  return skcArray.sort((a, b) => b.skc - a.skc).slice(0, 5);
}

const top5 = getTop5SKCByCountry(dynamics, 2024)

</script>

<template>
  <section class="card">
    <h3>Средняя контрактная цена импорта за 2024 год (топ-5)</h3>

    <v-list>
      <div v-for="i in top5" :key="i.skc">
        <div class="flex-row justify-space-between ga-4" >
          <p>{{i.country}}</p>
          <b>{{ i.skc }} $/ед</b>
        </div>
        <v-divider/>
      </div>
    </v-list>
  </section>
</template>

<style lang="sass" scoped>
p
  margin: 0
b
  font-family: monospace;

</style>