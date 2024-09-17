<script setup>
import FormSelect from './templates/FormSelect.vue';

import { ref, onMounted } from 'vue';

// Define emits correctly
const emit = defineEmits(['route-id']);

const routes = ref({ feederBus: [], rapidKL: [] });
const selectedBusType = ref('feederBus');  // New state for selected bus type

onMounted(() => {
  fetchAllRoutes();
});

const fetchAllRoutes = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/routes`);
    const responseData = await response.json();
    routes.value.feederBus = responseData.feeder_bus_active_routes;
    routes.value.rapidKL = responseData.rapid_kl_active_routes;

    console.log(routes.value);
  } catch (error) {
    console.error(error);
  }
};

const getRouteId = routeId => {
  // Use emit to trigger the event
  emit('route-id', routeId);
};

const setSelectedBusType = (busType) => {
  selectedBusType.value = busType;
};
</script>

<template>
  <div>
    <!-- Radio buttons to select bus type -->
    <div class="mb-4 flex space-x-4">
      <label class="flex items-center space-x-2">
        <input
          type="radio"
          value="feederBus"
          v-model="selectedBusType"
          class="text-blue-600 focus:ring-blue-500"
        />
        <span>MRT Feeder Bus</span>
      </label>
      <label class="flex items-center space-x-2">
        <input
          type="radio"
          value="rapidKL"
          v-model="selectedBusType"
          class="text-blue-600 focus:ring-blue-500"
        />
        <span>Rapid KL</span>
      </label>
    </div>

    <!-- Bus route dropdown based on selected type -->
    <FormSelect
      v-if="selectedBusType === 'feederBus' && routes.feederBus.length"
      id="search-bus"
      placeholder="Search for MRT Feeder Bus"
      :options="routes.feederBus.map(({ route_id }) => route_id)"
      @change="getRouteId"
    />

    <FormSelect
      v-if="selectedBusType === 'rapidKL' && routes.rapidKL.length"
      id="search-bus"
      placeholder="Search for Rapid KL Bus"
      :options="routes.rapidKL.map(({ route_id }) => route_id)"
      @change="getRouteId"
    />
  </div>
</template>

