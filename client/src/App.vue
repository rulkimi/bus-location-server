<script setup>
import BusMap from './components/BusMap.vue';
import BaseLayout from './layout/BaseLayout.vue';
import SearchControl from './components/SearchControl.vue';
import BusList from './components/BusList.vue';

import { ref } from 'vue';

const busMap = ref(null);
const buses = ref([]);
const currentRoute = ref('');
const loading = ref(false);

const setMapView = ({ latitude, longitude }) => {
  console.log('here')
  busMap.value.center = [latitude, longitude];
  busMap.value.zoom = 50;
  busMap.value.openMarkerPopup(latitude, longitude);
}

const fetchLocation = async (routeId) => {
  currentRoute.value = routeId;
  loading.value = true;
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/vehicle/${routeId}`);
    const responseData = await response.json();
    buses.value = responseData.vehicles;
    setMapView(buses.value[0].latitude, buses.value[0].longitude)

    // if (!this.buses) this.noBusFound = true;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <BaseLayout>
    <template #top-left>
      <div class="flex flex-col gap-4 bg-gray-400 p-6 h-full rounded-lg bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 hover:bg-opacity-50 transition-all duration-300">
        <SearchControl @route-id="fetchLocation" />
        <div v-if="currentRoute && loading" class="mt-2 animate-pulse">
          Searching for <font-awesome-icon class="text-blue-500" :icon="['fas', 'route']" /> <span class="text-blue-500">{{ currentRoute }}</span>
        </div>
        <template v-if="!loading">
          <div v-if="currentRoute" class="mt-2">
            <font-awesome-icon class="text-blue-500" :icon="['fas', 'route']" /> <span class="text-blue-500">{{ currentRoute }}</span> {{ buses.length > 1 ? 'buses' : 'bus' }}:
          </div>
          <BusList v-if="buses.length" :buses="buses" @bus-selected="setMapView" />
        </template>
      </div>
    </template>
    <BusMap :buses="buses" ref="busMap" />
  </BaseLayout>
</template>
