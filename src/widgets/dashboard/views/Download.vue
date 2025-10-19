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
      <h3>Сформировать обращение
        <v-tooltip open-on-hover location="top">
          <template v-slot:activator="{props}">
            <v-icon v-bind="props" icon="mdi-tooltip-question-outline" class="ml_5" color="primary"></v-icon>
          </template>
          Обращение будет сформировано с помощью искусственного интеллекта
        </v-tooltip>
      </h3>
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