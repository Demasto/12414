<script setup lang="ts">

const navItems = [
  // {
  //   title: 'Статистика',
  //   icon: 'mdi-finance',
  //   path: '/',
  // },
  // {
  //   title: 'Карта мира',
  //   icon: 'mdi-map-marker-radius',
  //   path: '/map',
  // },

  {
    title: 'ЕАИС',
    icon: 'mdi-list-box-outline',
    path: '/',
  },
  {
    title: 'Формирование обращения',
    icon: 'mdi-factory',
    path: '/industry',
  },
  // {
  //   title: 'О проекте',
  //   icon: 'mdi-information-variant',
  //   path: '/about',
  // },
]

</script>

<template>
  <v-list dense color="primary" nav density="compact" slim>
    <v-list-item
      v-for="item in navItems"
      link
      active-class="selected"
      :prepend-icon="item.icon"
      :to="item.path"
      :title="item.title"
      :key="item.path"
    />
  </v-list>
</template>

<style scoped lang="sass">

</style>
