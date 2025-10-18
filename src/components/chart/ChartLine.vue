<script setup lang="ts">
import {ref} from 'vue'
import type {ByYear} from "@/services/goods/GoodsAPI.ts";

const {dynamics = [], name} = defineProps<{
  dynamics: ByYear[]
  name: string
}>()

const options = ref({
  chart: {
    id: name
  },
  xaxis: {
    categories: dynamics.map(d => d.year)
  },
  colors: ['#667eea', '#3eba64', '#feb019', '#ff4560', '#008ffb', '#7f42e1']
})

const series = ref( [
  {
    name: name,
    data: dynamics.map(d => d.value_usd_mln)
  },
  // {
  //   name: 'series-2',
  //   data: [15, 40, 33, 52, 2, 25]
  // }
])
</script>

<template>
  <apexchart type="bar" :options="options" :series="series"></apexchart>
</template>



<style>

</style>