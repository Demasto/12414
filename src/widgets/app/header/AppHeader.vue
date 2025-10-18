<script setup lang="ts">
import {useDrawer} from "@/app/stores";
import {useDisplay} from "vuetify";

const drawer = useDrawer()
const {mobile} = useDisplay()
</script>

<template>
  <v-app-bar :absolute="!mobile">
    <template #prepend>
      <v-app-bar-nav-icon @click.stop="drawer.show = !drawer.show"/>
    </template>
  </v-app-bar>
</template>

<style scoped>

</style>