<script setup lang="ts">
import RoutesList from './RoutesList.vue'
const show = defineModel<boolean>()
</script>

<template>
  <v-navigation-drawer
    v-model="show"
    style="background: white;"
    temporary
    scrim
    mobile
  >
    <routes-list/>
  </v-navigation-drawer>
</template>

<style scoped lang="sass">
</style>
