<script setup lang="ts">

//TODO Выгрузка справки в формате PDF
import ProductCode from "./views/ProductCode.vue";
import RateCurrent from "./views/RateCurrent.vue";
import RateRequired from "./views/RateRequired.vue";
import DynamicsImport from "./views/DynamicsImport.vue";
import DynamicsProduction from "./views/DynamicsProduction.vue";
import DynamicsConsumption from "./views/DynamicsConsumption.vue";
import GeoImportStructure from "./views/GeoImportStructure.vue";
import AverageImportPrice from "./views/AverageImportPrice.vue";
import Recommendation from "./views/Recommendation.vue";
import type {ProductInfo} from "@/services/goods/GoodsAPI.ts";
import MapImport from "@/widgets/dashboard/views/MapImport.vue";
import Download from "@/widgets/dashboard/views/Download.vue";
import Chat from "@/widgets/dashboard/views/Chat.vue";
import JsonAbout from "@/widgets/dashboard/views/JsonAbout.vue";

defineProps<{
  info: ProductInfo
}>()

</script>

<template>
  <div>
    <v-row>
      <v-col>
        <product-code :name="info.good.name" :code="info.good.hs_code"/>
      </v-col>

    </v-row>

    <v-row>
      <v-col>
        <recommendation :info="info"/>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <rate-current :percent="info.tariffs[0].applied_rate * 100"/>
      </v-col>
      <v-col>
        <rate-required :percent="info.tariffs[0].wto_bound_rate * 100"/>
      </v-col>
    </v-row>

    <v-row>
      <v-col><dynamics-import :dynamics="info.imports"/></v-col>
      <v-col><dynamics-production :dynamics="info.production"/></v-col>
      <v-col><dynamics-consumption :dynamics="info.consumption"/></v-col>
    </v-row>

    <v-row>
      <v-col>
        <geo-import-structure :dynamics="info.imports"/>
      </v-col>

      <v-col>
        <average-import-price :dynamics="info.imports"/>
      </v-col>
    </v-row>

    <v-row>

      <v-col>
        <Download :id="info.good.id"/>
      </v-col>

    </v-row>

    <v-row>
      <v-col>
        <chat  :id="info.good.id"/>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <map-import :dynamics="info.imports"/>
      </v-col>
    </v-row>
  </div>
</template>

<style lang="sass" scoped>
//.dashboard
  //display: grid
  //grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))
</style>