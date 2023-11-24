
<template>
  <div class="relative my-2">
    <div class="absolute inset-0 flex items-center" aria-hidden="true">
      <div class="w-full border-t border-gray-300" />
    </div>
    <div class="relative flex justify-start">
      <span class="bg-white pr-3 text-base font-semibold leading-6 text-gray-900">{{ title}}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(['title'])
</script>
<style scoped>

</style>