<script setup lang="ts">
// Потребления
import ChartLine from "@/components/chart/ChartLine.vue";
import type {ByYear} from "@/services/goods/GoodsAPI.ts";

defineProps<{
  dynamics: ByYear[]
}>()
</script>

<template>
  <section class="card">
    <h3>Объём и динамика потребления</h3>
    <chart-line :dynamics="dynamics" name="Объём и динамика потребления (млн. $)"/>
  </section>
</template>

<style scoped>

</style>