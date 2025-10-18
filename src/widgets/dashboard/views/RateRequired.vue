<script setup lang="ts">
defineProps<{percent: number}>()

</script>

<template>
  <div class="card flex-col">
    <h3>Ставка по обязательствам РФ в ВТО</h3>
    <span class="percent">{{ percent }}%</span>
    <small>Максимальная ставка, согласованная в рамках ВТО</small>
  </div>
</template>

<style lang="sass" scoped>
.percent
  font-size: 6rem
  color: #3eba64
</style>