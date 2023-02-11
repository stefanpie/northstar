import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

import hurricaneDataRaw from '@/assets/data/hurdat2_processed.json'

export const useTopStore = defineStore('topStore', () => {
  const hurricaneData = reactive(hurricaneDataRaw)
  const selectedHurricane = ref(null)

  const selectedHurricaneData = computed(() => {
    if (selectedHurricane.value) {
      return hurricaneData.value.find(
        (hurricane) => hurricane.id === selectedHurricane.value
      )
    }
    return null
  })

  function selectHurricane(id) {
    selectedHurricane.value = id
  }

  function getHurricaneData(id) {
    return hurricaneData.value.find((hurricane) => hurricane.id === id)
  }

  function searchHurricanes(year, name) {
    var filtered_ids_year = []
    var filtered_ids_name = []

    console.log(year, name)

    // {
    //   "AL011982": [
    //       {
    //           "atcf_code": "AL011982",
    //           "storm_name": "ALBERTO",
    //           "year": 1982,
    //           "month": 6,
    //           "day": 2,
    //           "hour": 18,
    //           "minute": 0,
    //           "record_id": "",
    //           "system_status": "TD",
    //           "latitude": 22.2,
    //           "longitude": -86.5,
    //           "max_sus_wind": 25.0,
    //           "min_pressure": 1004.0,
    //           "wind_radii_34_NE": -999.0,
    //           "wind_radii_34_SE": -999.0,
    //           "wind_radii_34_SW": -999.0,
    //           "wind_radii_34_NW": -999.0,
    //           "wind_radii_50_NE": -999.0,
    //           "wind_radii_50_SE": -999.0,
    //           "wind_radii_50_SW": -999.0,
    //           "wind_radii_50_NW": -999.0,
    //           "wind_radii_64_NE": -999.0,
    //           "wind_radii_64_SE": -999.0,
    //           "wind_radii_64_SW": -999.0,
    //           "wind_radii_64_NW": -999.0,
    //           "delta_distance": 83.10604559029493,
    //           "azimuth": 48.11432134948142,
    //           "x": -0.021978178722422005,
    //           "y": -0.2061682588811092,
    //           "day_of_year": 153,
    //           "minute_of_day": 1080,
    //           "aday": 66910.49509128621,
    //           "vpre": 25100.0,
    //           "landfall": 0
    //       },
    //       {

    if (name != '') {
      // llop though keys
      for (var key in hurricaneData.value) {
        data_0 = hurricaneData.value[key][0]
        if (data_0.storm_name.startsWith(name)) {
          filtered_ids_name.push(key)
        }
      }
    } else {
      filtered_ids_name = Object.keys(hurricaneData.value)
    }

    if (year != '') {
      // llop though keys
      for (var key in hurricaneData.value) {
        data_0 = hurricaneData.value[key][0]
        if (data_0.year == year) {
          filtered_ids_year.push(key)
        }
      }
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
    searchHurricanes,
  }
})
