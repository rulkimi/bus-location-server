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
const isExpanded = ref(true);
const routes = ref({ feederBus: [], rapidKL: [] });
const errorMessage = ref('');
const errorTimeout = ref();

onMounted(() => {
  fetchAllRoutes();
});

const showError = message => {
  if (clearTimeout.value) clearTimeout(clearTimeout.value);

  errorMessage.value = message;
  errorTimeout.value = setTimeout(() => {
    errorMessage.value = '';
  }, 5000);
};

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
};

const fetchAllRoutes = async () => {
  serverLoading.value = true;
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/routes`);

    if (!response.ok) {
      showError('An error occured while fetching buses. Please refresh the page.');
    }

    const responseData = await response.json();
    const { feeder_bus_active_routes, rapid_kl_active_routes } = responseData;

    routes.value.feederBus = feeder_bus_active_routes;
    routes.value.rapidKL = rapid_kl_active_routes;

  } catch (error) {
    showError('An error occured while fetching buses. Please refresh the page.');
  } finally {
    serverLoading.value = false;
  }
};

const setMapView = ({ latitude, longitude }) => {
  busMap.value.center = [latitude, longitude];
  busMap.value.zoom = 50;
  busMap.value.openMarkerPopup(latitude, longitude);
};

const fetchLocation = async (routeId) => {
  currentRoute.value = routeId;
  loading.value = true;
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/vehicle/${routeId}`);

    if (!response.ok) {
      showError(`An error occured while fetching bus location for route ${routeId}. Please try again.`);
    }

    const responseData = await response.json();
    buses.value = responseData.vehicles;

    setMapView(buses.value[0].latitude, buses.value[0].longitude);

  } catch (error) {
    showError(`An error occured while fetching bus location for route ${routeId}. Please try again.`);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <BaseLayout>
    <template #top-left>
      <section
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
            <button
              v-if="buses.length"
              class="text-gray-400 cursor-pointer hover:scale-110 transition-all duration-300"
              @click="toggleExpand"
            >
              <font-awesome-icon v-if="isExpanded" :icon="['fas', 'compress']" />
              <font-awesome-icon v-else :icon="['fas', 'expand']" />
            </button>
          </template>
        </SearchControl>
      
        <div>
          <div v-if="currentRoute && loading" class="animate-pulse">
            Searching for <font-awesome-icon class="text-blue-500" :icon="['fas', 'route']" /> <span class="text-blue-500">{{ currentRoute }}</span> buses...
          </div>
          <div v-else-if="errorMessage" class="text-red-500" :class="currentRoute ? 'mb-4' : 'mt-4'">{{ errorMessage }}</div>
          <template v-if="!loading && isExpanded">
            <div v-if="currentRoute" class="mb-4">
              <font-awesome-icon class="text-blue-500" :icon="['fas', 'route']" /> <span class="text-blue-500">{{ currentRoute }}</span> {{ buses.length > 1 ? 'buses' : 'bus' }}:
            </div>
            <BusList v-if="buses.length" :buses="buses" @bus-selected="setMapView" />
          </template>
        </div>

      </section>
    </template>

    <BusMap :server-loading="serverLoading" :buses="buses" ref="busMap" />

    <section v-if="serverLoading" class="absolute top-0 left-0 w-full h-full flex justify-center items-center text-center p-4">
      <div class="max-w-[1280px]">
        <article class="flex flex-col gap-4">

          <div class="animate-pulse">
            <h1 class="text-xl md:text-2xl font-bold">We're currently using the free tier of Render.com.</h1>
            <p class="text-lg md:text-xl">Please be patient while the server loads.</p>
            <p class="text-lg md:text-xl hidden md:block">While you wait, feel free to get familiar with the UI. You can search for buses in the top-left corner.</p>
            <p class="text-lg md:text-xl">You’ll be able to track your bus location soon.</p>
          </div>

          <figure class="bg-white p-4 rounded-lg hidden md:block relative">
            <img class="rounded-lg" src="./assets/sample-location.png" width="1000" alt="Sample bus location">
            <figcaption class="text-lg md:text-xl text-center sr-only">Sample bus location image</figcaption>
          </figure>
          
        </article>
      </div>
    </section>

  </BaseLayout>
</template>
