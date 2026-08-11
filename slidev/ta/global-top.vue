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
        title: String(frontmatter.menuTitle ?? frontmatter.title ?? slide.meta.title ?? `Section ${index + 1}`),
        detail: String(frontmatter.menuDetail ?? 'Toolkit section'),
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
  <div v-if="!isPrintMode" class="toolkit-menu-layer">
    <button
      class="toolkit-menu-trigger"
      type="button"
      aria-label="Open toolkit map (M)"
      :aria-expanded="isOpen"
      @click="isOpen = true"
    >
      <span class="toolkit-menu-icon" aria-hidden="true"><i /><i /><i /></span>
      <span>Map</span>
      <kbd>M</kbd>
    </button>

    <Transition name="toolkit-menu">
      <div
        v-if="isOpen"
        class="toolkit-menu-backdrop"
        @click.self="closeContents"
      >
        <section
          class="toolkit-menu-panel"
          role="dialog"
          aria-modal="true"
          aria-labelledby="toolkit-menu-title"
        >
          <header>
            <div>
              <p>CCGL9065 · TA TOOLKIT</p>
              <h2 id="toolkit-menu-title">Session map</h2>
            </div>
            <button
              ref="closeButton"
              class="toolkit-menu-close"
              type="button"
              aria-label="Close map"
              @click="closeContents"
            >
              ×
            </button>
          </header>

          <nav aria-label="Toolkit sections">
            <button
              v-for="(section, index) in sections"
              :key="section.route"
              class="toolkit-menu-item"
              :class="{ active: activeSection === index }"
              type="button"
              :aria-current="activeSection === index ? 'location' : undefined"
              @click="jumpTo(section.route)"
            >
              <span class="toolkit-menu-number">{{ section.number }}</span>
              <span class="toolkit-menu-copy">
                <strong>{{ section.title }}</strong>
                <small>{{ section.detail }}</small>
              </span>
              <span aria-hidden="true">→</span>
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

<style>
.toolkit-menu-layer {
  position: fixed;
  z-index: 60;
  inset: 0;
  pointer-events: none;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.toolkit-menu-trigger {
  position: absolute;
  top: 22px;
  right: 28px;
  display: flex;
  gap: 9px;
  align-items: center;
  min-height: 39px;
  padding: 0 12px;
  border: 1px solid rgba(16, 42, 67, 0.22);
  border-radius: 999px;
  background: rgba(251, 248, 241, 0.92);
  box-shadow: 0 5px 18px rgba(16, 39, 60, 0.08);
  color: #102a43;
  font: 700 13px/1 "Helvetica Neue", Helvetica, Arial, sans-serif;
  opacity: 0.72;
  pointer-events: auto;
  transition: opacity 120ms ease, transform 120ms ease;
}

.toolkit-menu-trigger:hover,
.toolkit-menu-trigger:focus-visible,
.toolkit-menu-trigger[aria-expanded="true"] {
  opacity: 1;
  transform: translateY(-1px);
}

.toolkit-menu-trigger:focus-visible,
.toolkit-menu-close:focus-visible,
.toolkit-menu-item:focus-visible {
  outline: 3px solid #efd77d;
  outline-offset: 3px;
}

.toolkit-menu-trigger kbd,
.toolkit-menu-panel kbd {
  display: inline-grid;
  min-width: 21px;
  height: 21px;
  padding: 0 4px;
  border: 1px solid rgba(16, 42, 67, 0.24);
  border-radius: 4px;
  place-items: center;
  background: rgba(255, 255, 255, 0.55);
  color: #5b6d7b;
  font: 700 10px/1 "SFMono-Regular", Consolas, monospace;
}

.toolkit-menu-icon {
  display: grid;
  gap: 3px;
  width: 14px;
}

.toolkit-menu-icon i {
  display: block;
  height: 1.5px;
  background: currentColor;
}

.toolkit-menu-backdrop {
  position: absolute;
  display: flex;
  inset: 0;
  justify-content: flex-end;
  padding: 22px;
  background: rgba(9, 24, 36, 0.53);
  backdrop-filter: blur(7px);
  pointer-events: auto;
}

.toolkit-menu-panel {
  display: flex;
  width: min(610px, calc(100vw - 44px));
  height: 100%;
  overflow: hidden;
  flex-direction: column;
  border: 1px solid rgba(16, 42, 67, 0.16);
  border-radius: 16px;
  background: #fbf8f1;
  box-shadow: 0 24px 70px rgba(4, 18, 28, 0.25);
  color: #102a43;
}

.toolkit-menu-panel header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 32px 36px 24px;
  border-bottom: 1px solid #c2cbd2;
}

.toolkit-menu-panel header p {
  margin: 0 0 8px;
  color: #c96753;
  font-size: 12px;
  font-weight: 760;
  letter-spacing: 0.13em;
}

.toolkit-menu-panel header h2 {
  margin: 0;
  font-size: 41px;
  font-weight: 670;
  letter-spacing: -0.035em;
  line-height: 1;
}

.toolkit-menu-close {
  display: grid;
  width: 38px;
  height: 38px;
  padding: 0 0 3px;
  border: 1px solid rgba(16, 42, 67, 0.22);
  border-radius: 50%;
  place-items: center;
  background: transparent;
  color: #102a43;
  font: 300 29px/1 Arial, sans-serif;
}

.toolkit-menu-panel nav {
  display: grid;
  overflow: auto;
  flex: 1;
  align-content: start;
  padding: 12px 20px;
}

.toolkit-menu-item {
  display: grid;
  grid-template-columns: 45px 1fr 24px;
  gap: 14px;
  align-items: center;
  width: 100%;
  min-height: 84px;
  padding: 13px 16px;
  border: 0;
  border-bottom: 1px solid rgba(194, 203, 210, 0.72);
  background: transparent;
  color: inherit;
  text-align: left;
}

.toolkit-menu-item:hover {
  background: rgba(239, 215, 125, 0.2);
}

.toolkit-menu-item.active {
  background: rgba(201, 103, 83, 0.1);
}

.toolkit-menu-number {
  color: #c96753;
  font: italic 16px/1 Georgia, "Times New Roman", serif;
}

.toolkit-menu-copy {
  display: grid;
  gap: 5px;
}

.toolkit-menu-copy strong {
  font-size: 19px;
  font-weight: 680;
  line-height: 1.12;
}

.toolkit-menu-copy small {
  color: #5b6d7b;
  font-size: 13px;
  line-height: 1.28;
}

.toolkit-menu-panel footer {
  display: flex;
  justify-content: space-between;
  padding: 16px 36px 18px;
  border-top: 1px solid #c2cbd2;
  color: #5b6d7b;
  font-size: 12px;
}

.toolkit-menu-enter-active,
.toolkit-menu-leave-active {
  transition: opacity 140ms ease;
}

.toolkit-menu-enter-active .toolkit-menu-panel,
.toolkit-menu-leave-active .toolkit-menu-panel {
  transition: transform 140ms ease;
}

.toolkit-menu-enter-from,
.toolkit-menu-leave-to {
  opacity: 0;
}

.toolkit-menu-enter-from .toolkit-menu-panel,
.toolkit-menu-leave-to .toolkit-menu-panel {
  transform: translateX(22px);
}

@media (max-width: 1100px) {
  .toolkit-menu-panel {
    width: min(760px, calc(100vw - 44px));
  }

  .toolkit-menu-item {
    min-height: 96px;
  }

  .toolkit-menu-copy strong {
    font-size: 22px;
  }

  .toolkit-menu-copy small {
    font-size: 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .toolkit-menu-trigger,
  .toolkit-menu-enter-active,
  .toolkit-menu-leave-active,
  .toolkit-menu-enter-active .toolkit-menu-panel,
  .toolkit-menu-leave-active .toolkit-menu-panel {
    transition: none;
  }
}
</style>
