<script setup>
import BusMap from './components/BusMap.vue';
import BaseLayout from './layout/BaseLayout.vue';
import SearchControl from './components/SearchControl.vue';
import BusList from './components/BusList.vue';

import { ref, onMounted } from 'vue';

const busMap = ref(null);
const buses = ref([]);
const currentRoute = ref('');
const loading = ref(false);
const serverLoading = ref(false);
const isExpanded = ref(true); // State for expandable content

const routes = ref({ feederBus: [], rapidKL: [] });

onMounted(() => {
  fetchAllRoutes();
});

const fetchAllRoutes = async () => {
  serverLoading.value = true;
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/routes`);
    const responseData = await response.json();
    routes.value.feederBus = responseData.feeder_bus_active_routes;
    routes.value.rapidKL = responseData.rapid_kl_active_routes;

    console.log(routes.value);
  } catch (error) {
    console.error(error);
  } finally {
    serverLoading.value = false;
  }
};

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
    setMapView(buses.value[0].latitude, buses.value[0].longitude);
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// Toggle expandable content
const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
};
</script>

<template>
  <BaseLayout>
    <template #top-left>
      <div
        v-if="!serverLoading"
        class="text-xs sm:text-base flex flex-col bg-gray-400 p-6 h-full rounded-lg bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-10 hover:bg-opacity-50 transition-all duration-300"
        :class="(isExpanded && buses.length) || (loading && currentRoute) ? 'gap-4' : 'gap-0'"
      >
        <SearchControl
          class="order-1 md:order-none"
          :routes="routes"
          @route-id="fetchLocation"
        >
          <template #expand-button>
            <!-- Toggle Button -->
            <button v-if="buses.length" @click="toggleExpand" class="text-gray-400 cursor-pointer hover:scale-110 transition-all duration-300">
              <font-awesome-icon v-if="isExpanded" :icon="['fas', 'compress']" />
              <font-awesome-icon v-else :icon="['fas', 'expand']" />
            </button>
          </template>
        </SearchControl>
      
        <!-- Transition for Expand/Collapse -->
        <div>
          <div v-if="currentRoute && loading" class="animate-pulse">
            Searching for <font-awesome-icon class="text-blue-500" :icon="['fas', 'route']" /> <span class="text-blue-500">{{ currentRoute }}</span> buses...
          </div>
          <template v-if="!loading && isExpanded">
            <div v-if="currentRoute" class="mb-4">
              <font-awesome-icon class="text-blue-500" :icon="['fas', 'route']" /> <span class="text-blue-500">{{ currentRoute }}</span> {{ buses.length > 1 ? 'buses' : 'bus' }}:
            </div>
            <BusList v-if="buses.length" :buses="buses" @bus-selected="setMapView" />
          </template>
        </div>
      </div>
    </template>
    <BusMap :server-loading="serverLoading" :buses="buses" ref="busMap" />
    <div v-if="serverLoading" class="absolute top-0 left-0 w-full h-full flex justify-center items-center text-center p-4">
      <div class="max-w-[1280px]">
        <div class="flex flex-col gap-4">
          <div class="animate-pulse">
            <div class="text-xl md:text-2xl font-bold">We're currently using the free tier of Render.com.</div>
            <div class="text-lg md:text-xl">Please be patient while the server loads.</div>
            <div class="text-lg md:text-xl hidden md:block">While you wait, feel free to get familiar with the UI. You can search for buses in the top-left corner.</div>
            <div class="text-lg md:text-xl">You’ll be able to track your bus location soon.</div>
          </div>
          <div class="bg-white p-4 rounded-lg hidden md:block">
            <img class="rounded-lg" src="./assets/sample-location.png" width="1000" alt="">
          </div>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>
