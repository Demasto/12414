import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueRouter from 'unplugin-vue-router/vite'
import Vuetify from 'vite-plugin-vuetify'
import {fileURLToPath, URL} from "node:url";

// https://vite.dev/config/

export default defineConfig({
  plugins: [
    vue(),
    VueRouter(),
    Vuetify({
      autoImport: true,
      styles: {
        configFile: 'src/app/styles/vuetify/settings.sass',
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@style': fileURLToPath(new URL('./src/app/styles', import.meta.url))
    },
    extensions: ['.json', '.ts', '.vue'],
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://26.243.180.190:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})