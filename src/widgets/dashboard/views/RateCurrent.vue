<script setup lang="ts">
defineProps<{percent: number}>()
</script>

<template>
  <div class="card flex-col">
    <h3>Текущая ставка таможенной пошлины</h3>
    <span class="percent">{{percent}}%</span>
    <small>Действующая ставка пошлины на импорт данного товара</small>
  </div>
</template>

<style lang="sass" scoped>
.percent
  font-size: 6rem
  color: #667eea
</style>