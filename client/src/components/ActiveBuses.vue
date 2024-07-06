<template>
  <div v-if="routes.length" class="w-full">
    <FormSelect
      v-model="selectedRoute"
      :id="id"
      :label="label"
      :options="routes"
      placeholder="Select a route"
      @change="fetchLocation"
    />
  </div>
</template>

<script>
import FormSelect from './templates/FormSelect.vue';

export default {
  components: {
    FormSelect
  },
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
  data() {
    return {
      selectedRoute: ''
    };
  },
  methods: {
    fetchLocation(route) {
      this.$emit('fetch-location', route);
    }
  }
}
</script>