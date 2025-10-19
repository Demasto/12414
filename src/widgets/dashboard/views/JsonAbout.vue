<script setup lang="ts">
defineProps<{json: object}>()
</script>

<template>

  <section class="card">
    <h3>Метрика обоснования выбора</h3>
<!--    <pre><code>{{json}}</code></pre>-->

    Нормативные флаги:
    <ul>
      <li>техрег/сертификация: нет (in_techreg = false)</li>
      <li>в перечне ПП № 1875: нет (in_pp1875 = false)</li>
      <li>в приказе № 4114: нет (in_order4114 = false)</li>
    </ul>
  </section>
</template>

<style scoped>
pre {
  background-color: #ededed;
  padding: 0.4rem;
  border-radius: 8px;
}
code {
  background: none
}

ul {
  padding: 0;
}
</style>