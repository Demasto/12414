/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
// import 'vuetify/styles'

import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { defaults } from "./defaults";
import { theme } from "./theme";

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        },
    },
    display: {
        mobileBreakpoint: 'md',
        thresholds: {
            xs: 280,  // мобильные устройства (телефоны) 280px - 479px
            sm: 480,  // большие телефоны / маленькие планшеты 480px - 767px
            md: 768,  // планшеты и небольшие ноутбуки
            lg: 1280, // стандартные мониторы (включая 1920x1080)
            xl: 1920, // большие мониторы и ультра-широкие экраны
        },
    },
    defaults,
    theme
})
