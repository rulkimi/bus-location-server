<script setup>
import FormSelect from './templates/FormSelect.vue';

import { ref, onMounted } from 'vue';

// Define emits correctly
const emit = defineEmits(['route-id']);  // Changed to 'route-id' to match the event

const routes = ref({});

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
</script>

<template>
  <div class="">
    <FormSelect
      v-if="routes.feederBus"
      id="search-bus"
      placeholder="Search for Bus"
      :options="routes.feederBus.map(({ route_id }) => route_id )"
      @change="getRouteId"
    />
  </div>
</template>
