<script setup lang="ts">

</script>

<template>
  <v-main>
    <v-container fluid class="container">
      <router-view/>
    </v-container>
  </v-main>
</template>

<style scoped>
.container {
  min-height: calc(100vh - 64px);
}
</style>