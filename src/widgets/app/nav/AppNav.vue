<script setup lang="ts">
import NavDrawerDesktop from './views/NavDrawerDesktop.vue'
import NavDrawerMobile from './views/NavDrawerMobile.vue'
import { useDisplay } from 'vuetify'
import {useDrawer} from '@/app/stores'

const { mobile } = useDisplay()
const drawer = useDrawer()

</script>

<template>
  <nav-drawer-mobile v-if="mobile" v-model="drawer.show"/>
  <nav-drawer-desktop v-else v-model="drawer.show"/>
</template>
