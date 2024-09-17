<script setup>
import FormSelect from './templates/FormSelect.vue';

import { ref, onMounted } from 'vue';

// Define emits correctly
const emit = defineEmits(['route-id']);
const selectedBusType = ref('feederBus');  // New state for selected bus type

defineProps({
  routes: Object
})

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
      searchable
      v-if="selectedBusType === 'feederBus'"
      id="search-bus"
      placeholder="Search for MRT Feeder Bus"
      :options="routes.feederBus.map(({ route_id }) => route_id)"
      @change="getRouteId"
    />

    <FormSelect
      searchable
      v-if="selectedBusType === 'rapidKL'"
      id="search-bus"
      placeholder="Search for Rapid KL Bus"
      :options="routes.rapidKL.map(({ route_id }) => route_id)"
      @change="getRouteId"
    />
  </div>
</template>

