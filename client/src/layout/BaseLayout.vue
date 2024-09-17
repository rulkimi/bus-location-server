<template>
  <div class="w-screen h-screen relative">
    <div class="fixed bottom-2 md:bottom-auto md:top-2 left-2 right-2 z-[9999] md:w-[400px]">
      <slot name="top-left"></slot>
    </div>
    <slot></slot>
  </div>
</template>