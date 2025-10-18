<script setup lang="ts">

import {GoodsAPI, type Product} from "@/services/goods/GoodsAPI.ts";
import {onMounted, ref} from "vue";

const products = ref<null|Product[]>(null)

onMounted(async () => {
  try {
    products.value = await GoodsAPI.getAll()
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <h1>Товары</h1>

  <v-progress-linear color="primary" v-if="!products"/>

  <v-row v-else>
    <v-col v-for="product in products" :key="product.id">
      <router-link class="card product-card flex-center active" :to="`/dashboard?id=${product.id}`">
        {{product.name}}
      </router-link>
    </v-col>
  </v-row>
</template>

<style lang="sass" scoped>
@use '@style/vars' as *

.product-card
  color: #7f42e1
  font-size: 22px
  height: 60px
  transition: 100ms
  &:hover
    scale: 1.02
    box-shadow: $shadow

</style>