<template>
  <l-map
    :key="mapKey"
    :zoom="zoom"
    :center="center"
    :style="mapStyle"
    :options="{ zoomControl: false }"
  >
    <l-tile-layer :url="url" :attribution="attribution" />
    <l-marker
      v-for="bus in buses"
      :key="bus.vehicle_id"
      :lat-lng="[bus.latitude, bus.longitude]"
      ref="markers"
    >
      <l-popup>
        <div class="py-2 flex flex-col gap-2 text-base md:text-lg">

          <!-- Vehicle ID -->
          <div class="flex justify-between text-xs md:text-sm text-gray-400">
            <div class="flex items-center gap-2">
              <span>{{ bus.route_id }} ({{ bus.vehicle_id }})</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-nowrap">{{ formatTime(bus.timestamp) }}</span>
            </div>
          </div>

          <!-- Location -->
          <div class="flex items-start gap-2 col-span-3">
            <span>{{ bus.location }}</span>
          </div>

          <!-- waze and google map -->
          <div class="flex gap-4">
            <div
              class="flex items-start gap-2 cursor-pointer hover:underline"
              @click="openWaze(bus.latitude, bus.longitude)"
            >
              <div>
                <font-awesome-icon :icon="['fab', 'waze']" />
              </div>
              <span>Waze</span>
            </div>
            <div
              class="flex items-center gap-2 cursor-pointer hover:underline text-nowrap"
              @click="openGoogleMap(bus.latitude, bus.longitude)"
            >
              <img src="../assets/google-map.png" width="12" alt="">
              <span>Google Maps</span>
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
import { formatTime } from "../utils";

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
    buses: Array,
    serverLoading: Boolean
  },
  watch: {
    buses(newValue) {
      if (!newValue) return;
      const firstBus = newValue[0];
      this.center = [firstBus.latitude, firstBus.longitude];

      this.$nextTick(() => this.openMarkerPopup(firstBus.latitude, firstBus.longitude));
    },
    serverLoading(newValue) {
      this.$nextTick(() => {
        this.mapKey += 1;
      });
    },
  },
  data() {
    return {
      center: [2.922682, 101.64256],
      zoom: 50,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      mapKey: 0
    };
  },
  computed: {
    mapStyle() {
      return {
        height: '100%',
        width: '100%',
        filter: `blur(${this.serverLoading ? '6px' : '0px'})`
      };
    }
  },
  methods: {
    formatTime,
    openMarkerPopup(latitude, longitude) {
      const markers = this.$refs.markers;
      if (!markers) return;

      const markerInstance = markers.find(marker =>
        marker.$props.latLng[0] === latitude &&
        marker.$props.latLng[1] === longitude
      );

      if (markerInstance && markerInstance.leafletObject) {
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

