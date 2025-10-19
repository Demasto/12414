<script setup lang="ts">
// import {useRoute, useRouter} from "vue-router";
import {onMounted,   ref} from "vue";
import {GoodsAPI, type Product, type ProductInfo} from "@/services/goods/GoodsAPI.ts";
import ProductDashboard from "@/widgets/dashboard/ProductDashboard.vue";

// const route = useRoute()

// const router = useRouter()
// const _id = useRoute().query.id as string;

const dashboard = ref<ProductInfo|null>(null)
const all = ref<null|Product[]>(null)

const search = ref('')
const items = ref<Product[]>([])

const loading = ref<boolean>(false)

function onSearch() {
  if(!all.value) return
  items.value = all.value.filter(i => i.name.toLowerCase().includes(search.value.toLowerCase()))
}

async function onSelect(id: string) {
  loading.value = true
  try {
    dashboard.value = await GoodsAPI.get(id)
  }
  catch (error) {
    console.error(error)
  }
  loading.value = false
}

onMounted(async () => {
  try {
    all.value = await GoodsAPI.getAll()
    onSearch()
  }
  catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <v-text-field label="Поиск" density="compact" append-inner-icon="mdi-magnify" v-model="search" @keydown.enter="onSearch" @click:append-inner="onSearch"/>
  <v-list class="mb_30">
    <v-list-item v-for="(i, key) in items" :key="key" @click="onSelect(i.id)" density="compact">
      {{i.name}} ({{i.hs_code}})
    </v-list-item>
  </v-list>

  <v-divider class="mb_30" color="primary"/>


  <v-progress-linear color="primary" v-if="loading"/>
  <product-dashboard v-else-if="dashboard" :info="dashboard" />
</template>

<style scoped>

</style>