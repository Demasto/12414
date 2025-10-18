<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<template>
  <div class="card recommendation">
    <h2 class="flex-row align-center ga-2"><v-icon size="36" icon="mdi-alert-circle" color="primary"/>Итоговая рекомендация</h2>
    <p>{{text}}</p>
  </div>
</template>

<style lang="sass" scoped>
.recommendation
  background-color: rgba(102, 126, 234, 0.2)

p
  margin: 0
</style>