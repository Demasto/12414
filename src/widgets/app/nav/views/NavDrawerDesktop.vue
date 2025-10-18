<script setup lang="ts">
import RoutesList from './RoutesList.vue'
const show = defineModel<boolean>()
</script>

<template>
  <v-navigation-drawer
    absolute
    :rail="show"
    app
    class="padding_nav"
    floating
    permanent
  >
    <routes-list/>
  </v-navigation-drawer>
</template>

<style scoped lang="sass">

.padding_nav
  background: white
  //padding: 0 0 0 0.5rem

      //rail-width="90"

</style>
