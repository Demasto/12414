<script setup lang="ts">
import type {ImportsByYear} from "@/services/goods/GoodsAPI.ts";
import {GeoMap} from "@/widgets/geomap";
const {dynamics = []} = defineProps<{
  dynamics: ImportsByYear[]
}>()


function filterImportsByYear(importItems: ImportsByYear[]) {
  return importItems
      .filter(item => item.year === 2024)
      .reduce((acc, item) => {
        acc[item.country] = item;
        return acc;
      }, {});
}


</script>

<template>
  <geo-map :dict="filterImportsByYear(dynamics)" />
</template>

<style scoped>

</style>