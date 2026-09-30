<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

const props = withDefaults(defineProps<{ seconds?: number }>(), {
  seconds: 300,
})

const remaining = ref(props.seconds)
const running = ref(false)
let interval: ReturnType<typeof setInterval> | undefined
let deadline = 0

// Five minute bands: slate, blue, green, orange, then red for the final minute.
const minuteColors = ['#102a43', '#2563eb', '#21854b', '#b45309', '#b42318']
const finished = computed(() => remaining.value <= 0)
const color = computed(() => {
  const band = Math.max(0, minuteColors.length - Math.ceil(remaining.value / 60))
  return minuteColors[Math.min(band, minuteColors.length - 1)]
})

const display = computed(() => {
  const minutes = Math.floor(remaining.value / 60)
  const seconds = remaining.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

function start() {
  if (running.value || remaining.value <= 0)
    return
  deadline = Date.now() + remaining.value * 1000
  running.value = true
  interval = setInterval(() => {
    // Use elapsed time so a delayed browser callback cannot extend the speech.
    remaining.value = Math.max(0, Math.ceil((deadline - Date.now()) / 1000))
    if (finished.value)
      stop()
  }, 250)
}

function stop() {
  running.value = false
  if (interval)
    clearInterval(interval)
  interval = undefined
}

function reset() {
  stop()
  remaining.value = props.seconds
}

onBeforeUnmount(stop)
</script>

<template>
  <div class="conversion-timer">
    <div v-if="finished" class="conversion-timer__finished" role="status">
      Time's Up!
    </div>
    <div v-else class="conversion-timer__display" :style="{ color }" role="timer">
      {{ display }}
    </div>
    <div class="conversion-timer__controls">
      <button v-if="!finished" type="button" :disabled="running" @click="start">{{ running ? 'Running…' : 'Start timer' }}</button>
      <button type="button" class="secondary" @click="reset">Reset</button>
    </div>
  </div>
</template>
