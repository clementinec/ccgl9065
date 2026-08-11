<script setup lang="ts">
import { lockShortcuts, useNav } from '@slidev/client'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const { currentSlideNo, go, isPrintMode, slides } = useNav()
const isOpen = ref(false)
const closeButton = ref<HTMLButtonElement>()
let unlockShortcuts: undefined | (() => void)

const sections = computed(() =>
  slides.value
    .filter(slide => Number(slide.meta.slide?.frontmatter.level) === 1)
    .map((slide, index) => {
      const frontmatter = slide.meta.slide?.frontmatter ?? {}
      return {
        number: String(index + 1).padStart(2, '0'),
        title: String(frontmatter.title ?? slide.meta.title ?? `Section ${index + 1}`),
        detail: String(frontmatter.menuDetail ?? 'Lecture section'),
        route: String(frontmatter.routeAlias ?? slide.no),
        start: slide.no,
      }
    }),
)

const activeSection = computed(() => {
  let active = 0
  sections.value.forEach((section, index) => {
    if (currentSlideNo.value >= section.start)
      active = index
  })
  return active
})

function isEditableTarget(target: EventTarget | null) {
  const element = target as HTMLElement | null
  return Boolean(
    element
    && (element.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(element.tagName)),
  )
}

function closeContents() {
  isOpen.value = false
}

function toggleContents() {
  isOpen.value = !isOpen.value
}

async function jumpTo(route: string) {
  closeContents()
  await go(route)
}

function handleKeydown(event: KeyboardEvent) {
  if (isEditableTarget(event.target) || event.metaKey || event.ctrlKey || event.altKey)
    return

  if (event.key.toLowerCase() === 'm') {
    event.preventDefault()
    toggleContents()
  }
  else if (event.key === 'Escape' && isOpen.value) {
    event.preventDefault()
    closeContents()
  }
}

watch(isOpen, async (open) => {
  if (open) {
    unlockShortcuts = lockShortcuts()
    await nextTick()
    closeButton.value?.focus()
  }
  else {
    unlockShortcuts?.()
    unlockShortcuts = undefined
  }
})

onMounted(() => window.addEventListener('keydown', handleKeydown))
onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
  unlockShortcuts?.()
})
</script>

<template>
  <div v-if="!isPrintMode" class="ccgl-contents-layer">
    <button
      class="ccgl-contents-trigger"
      type="button"
      aria-label="Open contents (M)"
      :aria-expanded="isOpen"
      @click="isOpen = true"
    >
      <span class="ccgl-contents-icon" aria-hidden="true"><i /><i /><i /></span>
      <span>Contents</span>
      <kbd>M</kbd>
    </button>

    <Transition name="ccgl-contents">
      <div
        v-if="isOpen"
        class="ccgl-contents-backdrop"
        @click.self="closeContents"
      >
        <section
          class="ccgl-contents-panel"
          role="dialog"
          aria-modal="true"
          aria-labelledby="ccgl-contents-title"
        >
          <header class="ccgl-contents-header">
            <div>
              <p>CCGL9065 · LECTURE MAP</p>
              <h2 id="ccgl-contents-title">Contents</h2>
            </div>
            <button
              ref="closeButton"
              class="ccgl-contents-close"
              type="button"
              aria-label="Close contents"
              @click="closeContents"
            >
              <span aria-hidden="true">×</span>
            </button>
          </header>

          <nav aria-label="Lecture sections">
            <button
              v-for="(section, index) in sections"
              :key="section.route"
              class="ccgl-contents-item"
              :class="{ active: activeSection === index }"
              type="button"
              :aria-current="activeSection === index ? 'location' : undefined"
              @click="jumpTo(section.route)"
            >
              <span class="ccgl-contents-number">{{ section.number }}</span>
              <span class="ccgl-contents-copy">
                <strong>{{ section.title }}</strong>
                <small>{{ section.detail }}</small>
              </span>
              <span class="ccgl-contents-arrow" aria-hidden="true">→</span>
            </button>
          </nav>

          <footer>
            <span>{{ currentSlideNo }} / {{ slides.length }}</span>
            <span><kbd>M</kbd> or <kbd>Esc</kbd> to close</span>
          </footer>
        </section>
      </div>
    </Transition>
  </div>
</template>
