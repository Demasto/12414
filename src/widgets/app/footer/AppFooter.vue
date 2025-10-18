<script setup lang="ts">
</script>

<template>
  <v-footer class="footer flex-row align-start flex-wrap">
    <div>
      <router-link to="/home">
        <h2 class="text-primary">Лого</h2>
      </router-link>
      <p>Copyright © 2025 РейлСтат</p>
      <p>Все права защищены</p>

      <div class="mt_20">
        <a href="mailto:support@example.ru">support@example.ru</a>

      </div>

    </div>

    <div>
      <h4>Компания</h4>
      <a href="/about">О нас</a>
      <a>Контакты</a>
    </div>


    <div>
      <h4>Политика сайта</h4>
      <a>Пользовательское соглашение</a>
      <a>Обработка персональных данных</a>
      <a>Публичная оферта</a>
    </div>
  </v-footer>
</template>

<style scoped lang="sass">
.footer
  z-index: 1006
  background: white
  justify-content: center
  gap: 6rem
  padding: 3rem 1rem

a
  font-size: 14px
  line-height: 2.4rem
  display: block

p
  font-size: 14px
  line-height: 1.8em


</style>

<style scoped>
  .a {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: red;
  }
</style>