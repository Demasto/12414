<script setup lang="ts">
import {ref} from "vue";
import {GoodsAPI} from "@/services/goods/GoodsAPI.ts";

const {id} = defineProps<{id: string}>()


const text = ref('')
const response = ref('')

const loading = ref<boolean>(false)
async function send() {
  loading.value = true
  try {
    const {answer} = await GoodsAPI.chat(id, text.value)
    response.value = answer
  } catch (error) {
    console.error(error)
  }
  loading.value = false
}

</script>

<template>
  <section class="card">
    <h3>ИИ &ndash; агент</h3>
    <small class="mb_20" style="display: block;">Сформулируйте вопрос по товару. ИИ &ndash; агент постарается вам помочь</small>
<!--    <v-text-field  variant="filled" append-icon="mdi-send" :clearable="false"/>-->
    <v-textarea v-model="text" :disabled="loading" label="Ваш вопрос" rows="7" base-color="primary" color="primary" no-resize hide-spin-buttons append-icon="mdi-send" icon-color="primary" @click:append="send"/>

    <v-scroll-x-reverse-transition>
      <v-progress-linear v-if="loading" color="primary"/>
      <div v-else-if="response" v-html="response"/>
    </v-scroll-x-reverse-transition>
  </section>
</template>

<style>

</style>