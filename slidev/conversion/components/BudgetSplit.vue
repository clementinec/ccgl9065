<script setup lang="ts">
import { computed, ref } from 'vue'

const climate = ref(50)
const space = computed(() => 100 - climate.value)
</script>

<template>
  <div class="budget-split">
    <p>Drag the slider to see the split:</p>
    <input v-model.number="climate" type="range" min="0" max="100">
    <div class="budget-split__columns">
      <div>
        <strong>CLIMATE</strong>
        <i :style="{ width: `${Math.max(climate, 2)}%` }" />
        <span>${{ climate }}B</span>
      </div>
      <div>
        <strong>SPACE</strong>
        <i :style="{ width: `${Math.max(space, 2)}%` }" />
        <span>${{ space }}B</span>
      </div>
    </div>
  </div>
</template>
