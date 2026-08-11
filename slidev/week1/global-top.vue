<script setup lang="ts">
import { lockShortcuts, useNav } from '@slidev/client'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const sections = [
  {
    number: '01',
    title: 'After we know',
    detail: 'Why climate response has not yet added up',
    route: 'opening',
  },
  {
    number: '02',
    title: 'Us vs. AI',
    detail: 'What generative AI is actually good at',
    route: 'us-vs-ai',
  },
  {
    number: '03',
    title: 'When average becomes abundant',
    detail: 'Plausibility, sameness and AI slop',
    route: 'average-abundant',
  },
  {
    number: '04',
    title: 'Abundance has two infrastructures',
    detail: 'Expert selection, energy and the cost-down bet',
    route: 'two-infrastructures',
  },
  {
    number: '05',
    title: 'The workforce bet',
    detail: 'Build and test both sides of the motion',
    route: 'workforce-bet',
  },
] as const

const { currentSlideNo, go, isPrintMode, slides } = useNav()
const isOpen = ref(false)
const closeButton = ref<HTMLButtonElement>()
let unlockShortcuts: undefined | (() => void)

const sectionStarts = computed(() =>
  sections.map(({ route }) =>
    slides.value.find(slide => slide.meta.slide?.frontmatter.routeAlias === route)?.no ?? 1,
  ),
)

const activeSection = computed(() => {
  let active = 0
  sectionStarts.value.forEach((start, index) => {
    if (currentSlideNo.value >= start)
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

function openContents() {
  isOpen.value = true
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
      @click="openContents"
    >
      <span class="ccgl-contents-icon" aria-hidden="true">
        <i />
        <i />
        <i />
      </span>
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
              <p>CCGL9065 · WEEK 01</p>
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
            <span>Choose a chapter to jump directly to it.</span>
            <span><kbd>M</kbd> or <kbd>Esc</kbd> to close</span>
          </footer>
        </section>
      </div>
    </Transition>
  </div>
</template>

<style>
.ccgl-contents-layer {
  position: fixed;
  z-index: 60;
  inset: 0;
  pointer-events: none;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.ccgl-contents-trigger {
  position: absolute;
  top: 24px;
  right: 28px;
  display: flex;
  gap: 10px;
  align-items: center;
  min-height: 40px;
  padding: 0 12px;
  border: 1px solid rgba(16, 42, 67, 0.18);
  border-radius: 999px;
  background: rgba(251, 248, 241, 0.9);
  box-shadow: 0 5px 18px rgba(16, 39, 60, 0.08);
  color: #102a43;
  font: 650 14px/1 "Helvetica Neue", Helvetica, Arial, sans-serif;
  letter-spacing: 0.01em;
  opacity: 0.66;
  pointer-events: auto;
  transition:
    opacity 120ms ease,
    border-color 120ms ease,
    transform 120ms ease;
}

.ccgl-contents-trigger:hover,
.ccgl-contents-trigger:focus-visible,
.ccgl-contents-trigger[aria-expanded="true"] {
  border-color: rgba(16, 42, 67, 0.42);
  opacity: 1;
  transform: translateY(-1px);
}

.ccgl-contents-trigger:focus-visible,
.ccgl-contents-close:focus-visible,
.ccgl-contents-item:focus-visible {
  outline: 3px solid #efd77d;
  outline-offset: 3px;
}

.ccgl-contents-trigger kbd,
.ccgl-contents-panel footer kbd {
  display: inline-grid;
  min-width: 22px;
  height: 22px;
  padding: 0 5px;
  border: 1px solid rgba(16, 42, 67, 0.22);
  border-radius: 5px;
  place-items: center;
  background: rgba(255, 255, 255, 0.62);
  color: #5b6d7b;
  font: 700 11px/1 "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.ccgl-contents-icon {
  display: grid;
  gap: 3px;
  width: 15px;
}

.ccgl-contents-icon i {
  display: block;
  height: 1.5px;
  border-radius: 2px;
  background: currentColor;
}

.ccgl-contents-backdrop {
  position: absolute;
  display: flex;
  inset: 0;
  justify-content: flex-end;
  padding: 22px;
  background: rgba(9, 24, 36, 0.52);
  backdrop-filter: blur(8px);
  pointer-events: auto;
}

.ccgl-contents-panel {
  display: flex;
  width: min(610px, calc(100vw - 44px));
  height: 100%;
  overflow: hidden;
  flex-direction: column;
  border: 1px solid rgba(16, 42, 67, 0.12);
  border-radius: 18px;
  background: #fbf8f1;
  box-shadow: 0 24px 70px rgba(4, 18, 28, 0.24);
  color: #102a43;
}

.ccgl-contents-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 34px 38px 25px;
  border-bottom: 1px solid #c2cbd2;
}

.ccgl-contents-header p {
  margin: 0 0 8px;
  color: #c96753;
  font-size: 12px;
  font-weight: 750;
  letter-spacing: 0.14em;
}

.ccgl-contents-header h2 {
  margin: 0;
  font-size: 42px;
  font-weight: 650;
  letter-spacing: -0.045em;
  line-height: 1;
}

.ccgl-contents-close {
  display: grid;
  width: 38px;
  height: 38px;
  padding: 0 0 3px;
  border: 1px solid rgba(16, 42, 67, 0.2);
  border-radius: 50%;
  place-items: center;
  background: transparent;
  color: #102a43;
  font: 300 30px/1 Arial, sans-serif;
}

.ccgl-contents-panel nav {
  display: grid;
  overflow: auto;
  flex: 1;
  align-content: start;
  padding: 12px 20px;
}

.ccgl-contents-item {
  display: grid;
  grid-template-columns: 45px 1fr 24px;
  gap: 14px;
  align-items: center;
  width: 100%;
  min-height: 88px;
  padding: 14px 16px;
  border: 0;
  border-bottom: 1px solid rgba(194, 203, 210, 0.72);
  background: transparent;
  color: inherit;
  text-align: left;
}

.ccgl-contents-item:hover {
  background: rgba(239, 215, 125, 0.2);
}

.ccgl-contents-item.active {
  background: rgba(201, 103, 83, 0.09);
}

.ccgl-contents-number {
  color: #c96753;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 16px;
  font-style: italic;
}

.ccgl-contents-copy {
  display: grid;
  gap: 5px;
}

.ccgl-contents-copy strong {
  font-size: 20px;
  font-weight: 680;
  letter-spacing: -0.015em;
  line-height: 1.1;
}

.ccgl-contents-copy small {
  color: #5b6d7b;
  font-size: 13px;
  line-height: 1.25;
}

.ccgl-contents-arrow {
  color: #7a8994;
  font-size: 20px;
  transition: transform 120ms ease;
}

.ccgl-contents-item:hover .ccgl-contents-arrow {
  transform: translateX(3px);
}

.ccgl-contents-panel footer {
  display: flex;
  justify-content: space-between;
  padding: 17px 38px 19px;
  border-top: 1px solid #c2cbd2;
  color: #5b6d7b;
  font-size: 12px;
}

.ccgl-contents-panel footer span:last-child {
  display: flex;
  gap: 6px;
  align-items: center;
}

.ccgl-contents-enter-active,
.ccgl-contents-leave-active {
  transition: opacity 140ms ease;
}

.ccgl-contents-enter-active .ccgl-contents-panel,
.ccgl-contents-leave-active .ccgl-contents-panel {
  transition: transform 140ms ease;
}

.ccgl-contents-enter-from,
.ccgl-contents-leave-to {
  opacity: 0;
}

.ccgl-contents-enter-from .ccgl-contents-panel,
.ccgl-contents-leave-to .ccgl-contents-panel {
  transform: translateX(22px);
}

@media (prefers-reduced-motion: reduce) {
  .ccgl-contents-trigger,
  .ccgl-contents-enter-active,
  .ccgl-contents-leave-active,
  .ccgl-contents-enter-active .ccgl-contents-panel,
  .ccgl-contents-leave-active .ccgl-contents-panel,
  .ccgl-contents-arrow {
    transition: none;
  }
}
</style>
