<script setup>
import BusMap from './components/BusMap.vue';
import BaseLayout from './layout/BaseLayout.vue';
import SearchControl from './components/SearchControl.vue';

import { ref } from 'vue';

const busMap = ref(null);
const buses = ref([]);

const setMapView = ({ latitude, longitude }) => {
  busMap.value.center = [latitude, longitude];
  busMap.value.zoom = 50;
  busMap.value.openMarkerPopup(latitude, longitude);
}

const fetchLocation = async routeId => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/vehicle/${routeId}`);
    const responseData = await response.json();
    buses.value = responseData.vehicles;
    setMapView(buses.value[0].latitude, buses.value[0].longitude)

    // if (!this.buses) this.noBusFound = true;
  } catch (error) {
    console.error(error);
  } finally {
    // this.loading = false;
  }
}
</script>

<template>
  <BaseLayout>
    <template #top-left>
      <SearchControl @route-id="fetchLocation" />
    </template>
    <BusMap :buses="buses" ref="busMap" />
  </BaseLayout>
</template>
