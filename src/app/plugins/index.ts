import type {App} from "vue";
import router from "./router";
import vuetify from "./vuetify";
import {pinia} from "./pinia";
import VueApexCharts from "vue3-apexcharts";

export default {
    install(app: App) {
        app
            .use(router)
            .use(pinia)
            .use(vuetify)
            .use(VueApexCharts)
    }
}