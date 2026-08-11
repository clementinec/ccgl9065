<script setup lang="ts">
import { computed, ref } from 'vue'

const props = withDefaults(defineProps<{ roles?: string }>(), {
  roles: '',
})

const groups = ['Group One', 'Group Two', 'Group Three', 'Group Four', 'Group Five', 'Group Six']
const isOpen = ref(false)
const assignments = ref<{ group: string, role: string }[]>([])
const roleList = computed(() => props.roles.split('|').map(role => role.trim()).filter(Boolean))

function shuffle<T>(values: T[]) {
  const copy = [...values]
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1))
    ;[copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]]
  }
  return copy
}

function assign() {
  const roles = shuffle(roleList.value)
  assignments.value = groups.map((group, index) => ({
    group,
    role: roles[index] ?? `Position ${index + 1}`,
  }))
  isOpen.value = true
}
</script>

<template>
  <div class="conversion-assignment">
    <p>Randomly pair the six working groups with today’s positions.</p>
    <button type="button" @click="assign">Start the assignment</button>

    <div v-if="isOpen" class="conversion-assignment__overlay">
      <section role="dialog" aria-modal="true" aria-labelledby="assignment-title">
        <header>
          <div>
            <span>ACTIVITY SETUP</span>
            <h2 id="assignment-title">Random group assignments</h2>
          </div>
          <button type="button" aria-label="Close assignments" @click="isOpen = false">×</button>
        </header>
        <ol>
          <li v-for="assignment in assignments" :key="assignment.group">
            <strong>{{ assignment.group }}</strong>
            <span>{{ assignment.role }}</span>
          </li>
        </ol>
      </section>
    </div>
  </div>
</template>
