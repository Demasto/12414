<script setup lang="ts">
import {onMounted, ref} from "vue";
import {GoodsAPI, type Product} from "@/services/goods/GoodsAPI.ts";
import {useProducts} from "@/app/stores/useProducts.ts";

const emit = defineEmits(['select'])

const products = useProducts()

const search = ref('')
const last = ref('')
const items = ref<Product[]>([])

const loading = ref<boolean>(false)


function onSearch() {
  if(!products.all) return
  last.value = JSON.stringify(search.value)
  items.value = products.all.filter(i => i.name.toLowerCase().includes(search.value.toLowerCase()))
}

async function onSelect(id: string) {
  loading.value = true
  try {
    const d = await GoodsAPI.get(id)
    emit("select", d)
  }
  catch (error) {
    console.error(error)
  }
  loading.value = false
}

onMounted(async () => {
  try {
    await products.read()
    onSearch()
  }
  catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <v-text-field label="Поиск" density="compact" append-inner-icon="mdi-magnify" v-model="search" @input="onSearch" @keydown.enter="onSearch" @click:append-inner="onSearch"/>

  <v-list class="mb_30">
    <v-list-item v-for="(i, key) in items" :key="key" @click="onSelect(i.id)" density="compact">
      {{i.name}} ({{i.hs_code}})
    </v-list-item>
    <v-list-item v-if="!items.length">
      Не найдено товаров по запросу {{last}}
    </v-list-item>
  </v-list>

  <v-progress-linear color="primary" class="mb_30" v-if="loading"/>
  <v-divider class="mb_30" color="primary" v-else/>

</template>

<style scoped>

</style>