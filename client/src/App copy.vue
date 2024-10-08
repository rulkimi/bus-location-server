<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="container mx-auto px-4 py-8">
      <!-- Available Routes List -->
      <!-- <div class="mt-4">
        <h1 class="text-2xl font-bold mb-4">Available Routes:</h1>
        <div v-if="routes.feederBus.length || routes.rapidKL.length" class="flex flex-col md:flex-row flex-start gap-4">
          <active-buses
            id="feeder-bus"
            label="MRT Feeder Bus"
            :routes="routes.feederBus.map(({ route_id }) => route_id )"
            @fetch-location="fetchLocation"
          />
          <active-buses
            id="rapid-kl"
            label="Rapid KL Bus"
            :routes="routes.rapidKL.map(({ route_id }) => route_id )"
            @fetch-location="fetchLocation"
          />
        </div>
        <div v-else class="animate-pulse flex flex-col md:flex-row flex-start gap-4">
          Just a moment while we set things up. The server is loading and will be ready soon. Thanks for your patience!
        </div>
      </div> -->

      <div class="mt-4">
        <h1 class="text-2xl font-bold mb-4">Bus Location</h1>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-6 rounded-lg">
          <!-- Left side (1/3 width on medium screens and larger) -->
          <div class="md:col-span-1">
            <div class="">
              <FormInput
                id="search-route"
                v-model="routeId"
                :placeholder="routes.length ? 'Search route ID here or click from the list above' : 'Please wait for the server to load.'"
                class="mb-4"
                :disabled="!routes.feederBus.length && !routes.rapidKL.length"
              ></FormInput>
              <button
                @click="fetchLocation(routeId)"
                class="bg-blue-500 text-white px-4 py-2 rounded-md w-full"
                :class="loading ? 'opacity-75' : 'hover:bg-blue-600'"
                :disabled="loading"
              >
                  Search
              </button>
              <bus-list
                v-if="buses"
                :buses="buses"
                @bus-selected="setMapView"
                class="mt-4"
              />
              <div v-else-if="noBusFound" class="my-4">No bus found for route: {{ routeId.toUpperCase() }}</div>
            </div>
          </div>
          <!-- Right side (2/3 width on medium screens and larger) -->
          <div class="md:col-span-3">
            <div class="rounded-lg">
              <bus-map :buses="buses" ref="busMap" class="h-96" />
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import ActiveBuses from './components/ActiveBuses.vue';
import BusMap from './components/BusMap.vue';
import BusList from './components/BusList.vue';
import FormInput from './components/templates/FormInput.vue';

export default {
  name: 'App',
  components: {
    BusMap,
    BusList,
    ActiveBuses,
    FormInput
  },
  data() {
    return {
      routeId: '',
      buses: [],
      routes: {
        feederBus: [],
        rapidKL: []
      },
      loading: false,
      noBusFound: false
    };
  },
  async mounted() {
    await this.fetchAllRoutes();
  },
  methods: {
    async fetchLocation(routeId) {
      this.loading = true;
      this.routeId = routeId;
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/vehicle/${routeId}`);
        const responseData = await response.json();
        this.buses = responseData.vehicles;

        if (!this.buses) this.noBusFound = true;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async fetchAllRoutes() {
      try {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/routes`);
        const responseData = await response.json();
        this.routes.feederBus = responseData.feeder_bus_active_routes;
        this.routes.rapidKL = responseData.rapid_kl_active_routes;
      } catch (error) {
        console.error(error);
      }
    },
    setMapView({ latitude, longitude, vehicleId }) {
      this.$refs.busMap.center = [latitude, longitude];
      this.$refs.busMap.zoom = 50;
      this.$refs.busMap.openMarkerPopup(latitude, longitude);
    },
    selectRoute(route) {
      this.routeId = route; // Set the selected route to the input field
    }
  }
};
</script>
