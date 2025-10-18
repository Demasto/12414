<script setup lang="ts">
// Производства
import ChartLine from "@/components/chart/ChartLine.vue";
import type {ByYear} from "@/services/goods/GoodsAPI.ts";

defineProps<{
  dynamics: ByYear[]
}>()
</script>

<template>
  <section class="card">
    <h3>Объём и динамика производства</h3>
    <chart-line :dynamics="dynamics" name="Объём и динамика производства (млн. $)" />
  </section>
</template>

<style scoped>

</style>