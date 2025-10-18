<script setup lang="ts">
defineProps<{
  name: string;
  code: string;
}>()
</script>

<template>
  <section class="card">
    <h2>Наименование товара</h2>
    <b class="text-primary">{{name}}</b>
    <code class="ml_15 text-no-wrap">{{code}}</code>
  </section>
</template>
