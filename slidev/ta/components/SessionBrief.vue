<script setup lang="ts">
import session from '../session.json'

withDefaults(defineProps<{ compact?: boolean }>(), {
  compact: false,
})
</script>

<template>
  <div class="session-brief" :class="{ compact }">
    <div>
      <span>Session</span>
      <strong>{{ session.week }}</strong>
    </div>
    <div>
      <span>Topic</span>
      <strong>{{ session.topic }}</strong>
    </div>
    <div v-if="!compact">
      <span>Current task</span>
      <strong>{{ session.currentTask }}</strong>
    </div>
    <div v-if="!compact">
      <span>Next prompt</span>
      <strong>{{ session.nextPrompt }}</strong>
    </div>
  </div>
</template>
