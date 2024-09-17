<template>
  <ul class="bus-list">
    <li
      v-for="bus in buses" :key="bus.vehicle_id" 
      @click="handleClick(bus.latitude, bus.longitude, bus.vehicle_id)"
      class="bg-white shadow-md rounded-lg mb-2 px-4 py-3 cursor-pointer hover:bg-gray-100 flex flex-col gap-2"
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
      <div class="text-gray-500 flex items-start gap-2">
        <div>
          <font-awesome-icon class="text-red-500" :icon="['fas', 'location-dot']" />
        </div>
        <span>{{ bus.location }}</span>
      </div>
    </li>
  </ul>
</template>


<script>
export default {
  emits: ['bus-selected'],
  name: 'BusList',
  props: {
    buses: Array
  },
  methods: {
    handleClick(latitude, longitude, vehicleId) {
      this.$emit('bus-selected', { latitude, longitude, vehicleId });
    }
  }
};
</script>

<style scoped>
/* No need for additional styles if using Tailwind for all styling */
</style>
