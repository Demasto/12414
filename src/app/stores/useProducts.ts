import {ref} from 'vue'
import { defineStore } from 'pinia'
import {GoodsAPI, type Product} from "../../services/goods/GoodsAPI.ts";

export const useProducts = defineStore('rwer', () => {
    const all = ref<null|Product[]>(null)

    async function read() {
        if(!all.value) {
            all.value = await GoodsAPI.getAll()
        }
    }

    return {
        all, read
    }
})
