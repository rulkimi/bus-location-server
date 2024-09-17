<script setup>
import { defineEmits, defineProps, ref, watch } from 'vue';

const emits = defineEmits(['bus-selected']);

const props = defineProps({
  buses: Array
});

const selectedBus = ref(null);

// Watch for changes in `props.buses` and update `selectedBus` to the first bus's ID
watch(() => props.buses, (newBuses) => {
  if (newBuses.length > 0) {
    selectedBus.value = newBuses[0].vehicle_id;
  }
}, { immediate: true });

const handleClick = (latitude, longitude, vehicleId) => {
  selectedBus.value = vehicleId; // Update the selectedBus
  emits('bus-selected', { latitude, longitude, vehicleId });
}
</script>

<template>
  <ul class="bus-list">
    <li
      v-for="bus in buses" :key="bus.vehicle_id" 
      @click="handleClick(bus.latitude, bus.longitude, bus.vehicle_id)"
      :class="[ 
        'bg-white shadow-md rounded-lg mb-2 px-4 py-3 cursor-pointer border-2 border-transparent hover:border-blue-500 flex flex-col gap-2',
        { 'bg-blue-50 !border-blue-500': bus.vehicle_id === selectedBus }
      ]"
    >
      
      <!-- Bus Vehicle ID -->
      <div class="flex justify-between">
        <div class="flex gap-2 items-center">
          <font-awesome-icon class="text-blue-500" :icon="['fas', 'bus-simple']" />
          <div class="text-lg font-semibold">
            {{ bus.vehicle_id }}
          </div>
        </div>
        <div class="flex items-center gap-2">
          <font-awesome-icon class="text-gray-500" :icon="['fas', 'clock']" />
          <span>{{ new Date(bus.timestamp * 1000).toLocaleTimeString('en-US', { timeZone: 'Asia/Kuala_Lumpur', hour: '2-digit', minute: '2-digit', hour12: true }) }}</span>
        </div>
      </div>

      <!-- Location with FontAwesome Icon -->
      <div class="text-gray-500 flex items-start gap-2" :class="{ '!text-black' : bus.vehicle_id === selectedBus }">
        <div>
          <font-awesome-icon class="text-red-500" :icon="['fas', 'location-dot']" />
        </div>
        <span>{{ bus.location }}</span>
      </div>
    </li>
  </ul>
</template>
