import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

import hurricaneDataRaw from '@/assets/data/hurdat2_processed.json'

export const useTopStore = defineStore('topStore', () => {
  const hurricaneData = ref(hurricaneDataRaw)
  const selectedHurricane = ref(null)

  const selectedHurricaneData = computed(() => {
    if (selectedHurricane.value) {
      return hurricaneData.value[selectedHurricane.value]
    } else {
      return null
    }
  })

  function selectHurricane(id) {
    selectedHurricane.value = id
  }

  function getHurricaneData(id) {
    var data = null
    Object.keys(hurricaneData.value).forEach((key) => {
      if (key === id) {
        data = {
          atcf_code: hurricaneData.value[key][0].atcf_code,
          name: hurricaneData.value[key][0].storm_name,
          year: hurricaneData.value[key][0].year,
        }
      }
    })
    return data
  }

  function searchHurricanes(name, year) {
    var filtered_ids_year = []
    var filtered_ids_name = []

    if (name !== '') {
      Object.keys(hurricaneData.value).forEach((key) => {
        var data_0 = hurricaneData.value[key][0]
        if (
          data_0.storm_name
            .trim()
            .toLowerCase()
            .startsWith(name.trim().toLowerCase())
        ) {
          filtered_ids_name.push(key)
        }
      })
    } else {
      filtered_ids_name = Object.keys(hurricaneData.value)
    }

    if (year !== '') {
      Object.keys(hurricaneData.value).forEach((key) => {
        var data_0 = hurricaneData.value[key][0]
        if (data_0.year === year) {
          filtered_ids_year.push(key)
        }
      })
    } else {
      filtered_ids_year = Object.keys(hurricaneData.value)
    }

    var filtered_ids = []
    filtered_ids = filtered_ids_year.filter((id) =>
      filtered_ids_name.includes(id)
    )

    return filtered_ids
  }

  return {
    selectedHurricane,
    selectedHurricaneData,
    selectHurricane,
    searchHurricanes,
    getHurricaneData,
  }
})
