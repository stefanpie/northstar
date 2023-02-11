<script setup>
import HurricaneMap from '@/components/HurricaneMap.vue'
import { useTopStore } from '../stores/store'
import { ref } from 'vue'

const topStore = useTopStore()

const h_name = ref('')
const h_year = ref('')

const results = ref([])
</script>

<template>
  <div class="home">
    <HurricaneMap />
    <div class="controls">
      <div class="c-hurricane">
        <h2>Select Hurricane</h2>
        <input
          type="text"
          name="h-name"
          id="h-name"
          placeholder="Name"
          v-model="h_name"
          v-on:input="results = topStore.searchHurricanes(h_name, h_year)"
        />
        <input
          type="number"
          name="h-year"
          id="h-year"
          min="1990"
          max="3000"
          placeholder="Year"
          v-model="h_year"
          v-on:input="results = topStore.searchHurricanes(h_name, h_year)"
        />
        <div class="search-results"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  grid-gap: 2rem;
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: 1fr 1fr;
  grid-template-areas: 'map controls';
}

.home > .hurricane-map {
  grid-area: 'map';
}

.home > .controls {
  grid-area: 'controls';
}

.controls {
  width: 100%;
}

.controls > .c-hurricane {
  grid-gap: 0.5rem;
  display: grid;
  grid-template-rows: auto auto auto;
  grid-template-columns: auto 1fr;
  grid-template-areas: 'title title' 'name results' 'year results';
}
.c-hurricane > h2 {
  grid-area: title;
}

.c-hurricane > #h-name {
  grid-area: name;
}

.c-hurricane > #h-year {
  grid-area: year;
}

.c-hurricane > .search-results {
  grid-area: results;
}
</style>
