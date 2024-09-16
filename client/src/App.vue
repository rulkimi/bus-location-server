<script setup>
import BusMap from './components/BusMap.vue';
import BaseLayout from './layout/BaseLayout.vue';
</script>

<template>
  <BaseLayout>
    <BusMap :buses="buses" ref="busMap" />
  </BaseLayout>
</template>
