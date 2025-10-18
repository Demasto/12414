<script setup lang="ts">
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {GoodsAPI, type ProductInfo} from "@/services/goods/GoodsAPI.ts";
import ProductDashboard from "@/widgets/dashboard/ProductDashboard.vue";

// const route = useRoute()

const id = useRoute().query.id

const dashboard = ref<ProductInfo|null>(null)

onMounted(async () => {
  try {
    dashboard.value = await GoodsAPI.get(id)
  }
  catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <div v-if="!id">
    Не указан ID
  </div>
  <v-progress-linear color="primary" v-else-if="!dashboard"/>
  <product-dashboard v-else :info="dashboard" />
</template>

<style scoped>

</style>