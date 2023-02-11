<template>
  <div class="hurricane-map">
    <LMap :zoom="zoom" :center="center">
      <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <div v-for="item in items" :key="item.id">
        {{ item }}
      </div>
    </LMap>
  </div>
</template>

<script setup>
import 'leaflet/dist/leaflet.css'
import { LMap, LTileLayer } from '@vue-leaflet/vue-leaflet'
import { ref } from 'vue'

const center = ref([30, -65])
const zoom = ref(4)
</script>

<style scoped></style>
