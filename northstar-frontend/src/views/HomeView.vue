<script setup>
import HurricaneMap from '@/components/HurricaneMap.vue'
import { useTopStore } from '../stores/store'
import { ref, onMounted } from 'vue'
import { createReturnStatement } from '@vue/compiler-core'

const topStore = useTopStore()

const h_name = ref('')
const h_year = ref('')

const results = ref([])
const results_data = ref([])

function updateResults() {
  results.value = topStore.searchHurricanes(h_name.value, h_year.value)
  results_data.value = results.value.map((h) => {
    return topStore.getHurricaneData(h)
  })
}
onMounted(() => {
  updateResults()
})
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
          v-on:input="updateResults()"
        />
        <input
          type="number"
          name="h-year"
          id="h-year"
          min="1990"
          max="3000"
          placeholder="Year"
          v-model="h_year"
          v-on:input="updateResults()"
        />
        <div class="search-results">
          <div
            v-for="item in results_data"
            :key="item.atcf_code"
            class="h-result"
            v-on:click="topStore.selectHurricane(item.atcf_code)"
            :class="{ selected: topStore.selectedHurricane === item.atcf_code }"
          >
            <p>{{ item.atcf_code }}</p>
            <p>{{ item.name }} - {{ item.year }}</p>
          </div>
        </div>
      </div>
      <div class="c-data">
        <h2>Data</h2>
        <div class="data-results">{{ topStore.selectedHurricaneData }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  height: 100%;
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
  overflow-y: auto;
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
  display: grid;
  grid-template-rows: repeat(auto-fill, 1fr);
  grid-template-columns: 1fr 1fr 1fr;
  grid-auto-rows: min-content;
  grid-auto-columns: 1fr;
  grid-auto-flow: row;
  grid-area: results;
  gap: 1rem;
  border: var(--bw) var(--bs) var(--ct-border);
  background-color: var(--ct-secondary);
  padding: 1rem;
  height: 15rem;
  overflow-y: auto;
}

.h-result {
  display: grid;
  grid-template-rows: 1fr 1fr;
  grid-template-areas: 'code' 'name' 'year';
  border: var(--bw) var(--bs) var(--ct-border);
  background-color: var(--ct-primary);
  padding: 0.5rem;
}

.h-result:hover,
.h-result:focus {
  background-color: var(--ct-secondary);
}

.h-result.selected {
  background-color: var(--ct-success);
}
</style>
