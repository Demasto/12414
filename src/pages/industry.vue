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
function flag(f: boolean) {
  return f ? 'Да' : 'Нет'
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



    <div class="flex-row ga-6 ">
      <v-text-field label="Email"/>
      <v-text-field label="Телефон"/>
    </div>

    <h3>Обоснование меры</h3>

    <ul class="mb_20" :key="dashboard.summary.delta_ns">
      <li>Год анализа: {{dashboard.summary.last_year}}</li>
      <li>Доля НС: {{dashboard.summary.share_ns.toFixed(1)}}%</li>
      <li>Изменение поставок НС к прошлому году: {{dashboard.summary.delta_ns.toFixed(1)}}</li>
      <!--      <li>Производство vs потребление: {{flag(info.summary.prod_ge_cons)}}</li>-->
      <!--      <li>Тарифы: {{info.summary.applied * 100}}%</li>-->
      <!--      <li>ВТО: {{info.summary.wto_bound * 100}}%</li>-->
      <!--      <li>Метрика расчёта импорта: {{info.summary.metric_used}}</li>-->
      <!--      <li>Логика выбора по методике: {{info.summary.branch}}</li>-->

      <li>техрег/сертификация: {{flag(dashboard.flags[0]?.sin_techreg)}}</li>
      <li>в перечне ПП № 1875: {{flag(dashboard.flags[0]?.in_pp1875)}}</li>
      <li>в приказе № 4114: {{flag(dashboard.flags[0]?.in_order4114)}}</li>

      <li>
        {{dashboard.summary.notes.join(', ')}}
      </li>
    </ul>

    <div class="flex-row justify-end">
      <div v-if="showSend && !showResult">
        🟢 Полнота: 92 %  🟡 Релевантность: ТТР

        <v-btn size="x-large" variant="outlined" class="ml_15"  @click="onSend" :loading="sendLoading">Сформировать обращение</v-btn>
      </div>

      <div v-else-if="showResult" class="card" style="width: 100%;">
        <h3>Ваш запрос отправлен!</h3>
        <p>Ожидайте обратной связи по электронной почте, указанной в форме!</p>
      </div>

      <v-btn v-else size="x-large" :loading="checkLoading" @click="onCheck">Проверить суть обращения</v-btn>
    </div>
  </section>
</template>

<style scoped>
ul {
  padding: 0
}

</style>