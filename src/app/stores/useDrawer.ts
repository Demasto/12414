import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDrawer = defineStore('drawer', () => {
    const show = ref(false)

    return { show }
})
