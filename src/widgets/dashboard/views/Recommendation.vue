<script setup lang="ts">
import type {ProductInfo} from "@/services/goods/GoodsAPI.ts";

const {info} = defineProps<{
  info: ProductInfo
}>()

function flag(f: boolean) {
  return f ? 'Да' : 'Нет'
}

const {in_techreg, in_order4114, in_pp1875} = info.flags[0]


</script>

<template>
  <div class="card recommendation">
    <h2 class="flex-row align-center ga-2"><v-icon size="36" icon="mdi-alert-circle" color="primary"/>Итоговая рекомендация</h2>
    <b>{{info.measures.join(', ')}}</b>

    <ul>
      <li>Год анализа: {{info.summary.last_year}}</li>
      <li>Доля НС: {{info.summary.share_ns.toFixed(1)}}%</li>
      <li>Изменение поставок НС к прошлому году: {{info.summary.delta_ns.toFixed(1)}}</li>
<!--      <li>Производство vs потребление: {{flag(info.summary.prod_ge_cons)}}</li>-->
<!--      <li>Тарифы: {{info.summary.applied * 100}}%</li>-->
<!--      <li>ВТО: {{info.summary.wto_bound * 100}}%</li>-->
<!--      <li>Метрика расчёта импорта: {{info.summary.metric_used}}</li>-->
<!--      <li>Логика выбора по методике: {{info.summary.branch}}</li>-->

      <li>техрег/сертификация: {{flag(in_techreg)}}</li>
      <li>в перечне ПП № 1875: {{flag(in_pp1875)}}</li>
      <li>в приказе № 4114: {{flag(in_order4114)}}</li>

      <li>
        {{info.summary.notes.join(', ')}}
      </li>
    </ul>
  </div>
</template>

<style lang="sass" scoped>
.recommendation
  background-color: rgba(102, 126, 234, 0.2)

ul
  padding: 0

p
  margin: 0
</style>