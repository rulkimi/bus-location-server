<script setup>
import FormSelect from './templates/FormSelect.vue';

import { ref } from 'vue';

const emit = defineEmits(['route-id']);
const selectedBusType = ref('feederBus');

defineProps({ routes: Object });

const getRouteId = routeId => emit('route-id', routeId);
</script>

<template>
  <div>
    <!-- Radio buttons to select bus type -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-4">
        <label for="mrt-feeder-bus" class="flex items-center space-x-2">
          <input
            id="mrt-feeder-bus"
            type="radio"
            value="feederBus"
            v-model="selectedBusType"
            class="text-blue-600 focus:ring-blue-500"
          />
          <span>MRT Feeder Bus</span>
        </label>
        <label for="rapid-kl" class="flex items-center space-x-2">
          <input
            id="rapid-kl"
            type="radio"
            value="rapidKL"
            v-model="selectedBusType"
            class="text-blue-600 focus:ring-blue-500"
          />
          <span>Rapid KL</span>
        </label>
      </div>
      <div class="absolute top-6 right-6">
        <slot name="expand-button"></slot>
      </div>
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

