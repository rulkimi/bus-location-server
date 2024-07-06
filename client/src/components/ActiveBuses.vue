<template>
  <div v-if="routes.length" class="w-full">
    <label :for="id + '-routes'" class="block text-sm font-medium text-gray-700">{{ label }}</label>
    <select
      :id="id + '-routes'"
      class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
      @change="fetchLocation($event.target.value)"
    >
      <option value="" disabled selected>Select a route</option>
      <option
        v-for="route in routes"
        :key="route"
        :value="route"
      >
        {{ route }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  emits: ['fetch-location'],
  props: {
    id: {
      type: String,
      required: true
    },
    label: {
      type: String,
      default: ''
    },
    routes: {
      type: Array,
      required: true
    }
  },
  methods: {
    fetchLocation(route) {
      this.$emit('fetch-location', route);
    }
  }
}
</script>