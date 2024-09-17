<template>
  <l-map :zoom="zoom" :center="center" style="height: 100%; width: 100%; border-radius: 6px;">
    <l-tile-layer :url="url" :attribution="attribution" />
    <l-marker
      v-for="bus in buses"
      :key="bus.vehicle_id"
      :lat-lng="[bus.latitude, bus.longitude]"
      ref="markers"
    >
      <l-popup>
        <div class="py-2 flex flex-col gap-2 text-lg">
          <!-- Vehicle ID -->
          <div class="flex justify-between text-sm text-gray-400">
            <div class="flex items-center gap-2">
              <!-- <font-awesome-icon class="text-blue-500" :icon="['fas', 'bus-simple']" /> -->
              <span>{{ bus.route_id }} ({{ bus.vehicle_id }})</span>
            </div>
            <!-- Route ID -->
            <!-- <div class="flex items-center gap-2">
              <font-awesome-icon class="text-green-500" :icon="['fas', 'route']" />
              <span>{{ bus.route_id }}</span>
            </div> -->
            <!-- Timestamp -->
            <div class="flex items-center gap-2">
              <!-- <font-awesome-icon class="text-gray-500" :icon="['fas', 'clock']" /> -->
              <span class="text-nowrap">{{ new Date(bus.timestamp * 1000).toLocaleTimeString('en-US', { timeZone: 'Asia/Kuala_Lumpur', hour: '2-digit', minute: '2-digit', hour12: true }) }}</span>
            </div>
          </div>

          <!-- Location -->
          <div class="flex items-start gap-2 col-span-3">
            <!-- <div>
              <font-awesome-icon class="text-red-500" :icon="['fas', 'map-marker-alt']" />
            </div> -->
            <span>{{ bus.location }}</span>
          </div>

          <!-- waze and google map -->
          <div class="flex gap-4">
            <div class="flex items-start gap-2 cursor-pointer hover:underline" @click="openWaze(bus.latitude, bus.longitude)">
              <div>
                <font-awesome-icon :icon="['fab', 'waze']" />
              </div>
              <span>Waze</span>
            </div>
            <div class="flex items-center gap-2 cursor-pointer hover:underline" @click="openGoogleMap(bus.latitude, bus.longitude)">
              <div>
                <img src="../assets/google-map.png" width="12" alt="">
              </div>
              <span>Google Map</span>
            </div>
          </div>
        </div>
      </l-popup>
    </l-marker>
    <l-control-zoom position="topright"></l-control-zoom>
  </l-map>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPopup, LControlZoom } from '@vue-leaflet/vue-leaflet';

export default {
  name: 'BusMap',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LControlZoom
  },
  props: {
    buses: Array
  },
  watch: {
    buses(newValue) {
      if (!newValue) return;
      const firstBus = newValue[0];
      this.center = [firstBus.latitude, firstBus.longitude];

      this.$nextTick(() => this.openMarkerPopup(firstBus.latitude, firstBus.longitude));
    }
  },
  data() {
    return {
      center: [2.922682, 101.64256],
      zoom: 50,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    };
  },
  methods: {
    openMarkerPopup(latitude, longitude) {
      const markers = this.$refs.markers;
      if (!markers) return;

      const markerInstance = markers.find(marker =>
        marker.$props.latLng[0] === latitude &&
        marker.$props.latLng[1] === longitude
      );

      if (markerInstance && markerInstance.leafletObject) {
        // open the popup associated with the marker using leafletObject
        markerInstance.leafletObject.openPopup();
      } else {
        console.error('Marker instance or leafletObject not found:', markerInstance);
      }
    },
    openWaze(latitude, longitude) {
      const wazeUrl = `https://waze.com/ul?ll=${latitude},${longitude}&navigate=yes`;
      window.open(wazeUrl, '_blank');
    },
    openGoogleMap(latitude, longitude) {
      const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${latitude},${longitude}`;
      window.open(googleMapsUrl, '_blank');
    },
  }
};
</script>
