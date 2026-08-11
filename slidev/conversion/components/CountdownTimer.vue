<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

const props = withDefaults(defineProps<{ seconds?: number }>(), {
  seconds: 300,
})

const remaining = ref(props.seconds)
const running = ref(false)
let interval: ReturnType<typeof setInterval> | undefined

const display = computed(() => {
  const minutes = Math.floor(remaining.value / 60)
  const seconds = remaining.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

function start() {
  if (running.value || remaining.value <= 0)
    return
  running.value = true
  interval = setInterval(() => {
    if (remaining.value > 0)
      remaining.value -= 1
    if (remaining.value <= 0)
      stop()
  }, 1000)
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
    <div class="conversion-timer__display" :class="{ urgent: remaining <= 60 }">
      {{ display }}
    </div>
    <div class="conversion-timer__controls">
      <button type="button" @click="start">{{ running ? 'Running…' : 'Start timer' }}</button>
      <button type="button" class="secondary" @click="reset">Reset</button>
    </div>
  </div>
</template>
