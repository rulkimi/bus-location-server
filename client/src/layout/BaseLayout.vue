<script setup>
import SearchControl from '../components/SearchControl.vue';
</script>

<template>
  <div class="w-screen h-screen relative">
    <div class="fixed top-2 left-2 z-[9999]">
      <SearchControl />
    </div>
    <slot></slot>
  </div>
</template>