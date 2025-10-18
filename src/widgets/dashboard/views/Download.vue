<script setup lang="ts">

const {id} = defineProps<{id: string}>()


</script>

<template>
  <div class="card ga-6">
    <div>
      <h3>Выгрузка данных</h3>
      <v-btn variant="elevated" :href="`/api/goods/${id}/report.docx`" prepend-icon="mdi-download" size="x-large">Справка по товару</v-btn>
    </div>
    <div>
      <h3>Сформировать обращение </h3>
      <v-btn prepend-icon="mdi-download" :href="`/api/goods/${id}/mosprom-letter.docx`" size="x-large" variant="outlined">Обращение в Моспром</v-btn>
    </div>
  </div>
</template>

<style lang="sass" scoped>
.card
  display: grid
  grid-template-columns: 1fr 1fr
  @media (max-width: 900px)
    display: flex
    flex-flow: row wrap
</style>