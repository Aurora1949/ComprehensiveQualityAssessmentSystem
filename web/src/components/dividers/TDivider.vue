<template>
  <div class="relative" :class="{'my-2': position === 'left'}">
    <div class="absolute inset-0 flex items-center" aria-hidden="true">
      <div class="w-full border-t border-gray-300"/>
    </div>
    <div class="relative flex justify-start"
         :class="{'justify-start': position==='left', 'justify-center': position==='center'}">
      <slot name="title">
        <span class="bg-white pr-3 text-base font-semibold leading-6 text-gray-900">{{ title }}</span>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps(['title', 'position'])
</script>
<style scoped>

</style>