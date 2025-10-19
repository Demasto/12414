<script setup lang="ts">

import Search from "@/components/Search.vue";
import {ref} from "vue";
import type {ProductInfo} from "@/services/goods/GoodsAPI.ts";
const dashboard = ref<ProductInfo|null>(null)


const checkLoading = ref<boolean>(false)
const showSend = ref<boolean>(false)
const sendLoading = ref<boolean>(false)
const showResult = ref<boolean>(false)

function onCheck() {
  checkLoading.value = true
  setTimeout(() => {
    checkLoading.value = false
    showSend.value = true
  }, 1000)
}

function onSend() {
  sendLoading.value = true
  setTimeout(() => {
    sendLoading.value = false
    showResult.value = true
  }, 1000)
}

</script>

<template>
  <Search class="mb_30" @select="d => dashboard = d"/>

  <section class="card" v-if="dashboard">
    <h1>Формирование обращения</h1>
    <p>Проверка полноты и релевантности инициатив предприятий с помощью ИИ</p>
    <v-text-field label="Организация"/>

    <div class="flex-row ga-6 ">
      <v-text-field label="ИНН"/>
      <v-text-field label="ОГРН"/>
    </div>

    <v-text-field label="Адрес" variant="underlined"/>

    <v-select label="Тема обращения" density="compact" variant="underlined" :items="['Жалоба', 'Предложение', 'Вопрос', 'Другое']"/>

    <v-text-field label="Суть обращения"  />
    <v-text-field label="Обоснование меры"  />

    <div class="flex-row ga-6 ">
      <v-text-field label="Email"/>
      <v-text-field label="Телефон"/>
    </div>

    <div class="flex-row justify-end">
      <v-btn size="x-large" variant="outlined" v-if="showSend && !showResult" @click="onSend" :loading="sendLoading">Сформировать обращение</v-btn>

      <div v-else-if="showResult" class="card" style="width: 100%;">
        <h3>Ваш запрос отправлен!</h3>
        <p>Ожидайте обратной связи по электронной почте, указанной в форме!</p>
      </div>

      <v-btn v-else size="x-large" :loading="checkLoading" @click="onCheck">Проверить суть обращения</v-btn>
    </div>
  </section>
</template>

<style scoped>

</style>