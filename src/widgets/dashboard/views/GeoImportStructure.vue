<script setup lang="ts">

import ChartPie from "@/components/chart/ChartPie.vue";
import type {ImportsByYear} from "@/services/goods/GoodsAPI.ts";

const {dynamics = []} = defineProps<{
  dynamics: ImportsByYear[]
}>()


</script>

<template>
  <div class="card">
    <h3>Географическая структура импорта</h3>
    <chart-pie :dynamics="dynamics" />
  </div>
</template>

<style scoped>

</style>