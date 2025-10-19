<script setup lang="ts">
import {ref} from "vue";
import {type ProductInfo} from "@/services/goods/GoodsAPI.ts";
import ProductDashboard from "@/widgets/dashboard/ProductDashboard.vue";
import Search from "@/components/Search.vue";
const dashboard = ref<ProductInfo|null>(null)

</script>

<template>
  <Search class="mb_30" @select="d => dashboard = d"/>
  <product-dashboard v-if="dashboard" :info="dashboard" />
</template>

<style scoped>

</style>