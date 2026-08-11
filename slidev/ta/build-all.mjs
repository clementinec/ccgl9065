import { spawnSync } from 'node:child_process'
import { rmSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const workingDirectory = fileURLToPath(new URL('.', import.meta.url))
const allDecks = ['tutorial', 'onboarding']
const requestedDecks = process.argv.slice(2)
const decks = requestedDecks.length ? requestedDecks : allDecks

for (const deck of decks) {
  if (!allDecks.includes(deck)) {
    process.stderr.write(`Unknown deck: ${deck}\n`)
    process.exit(1)
  }
}

for (const deck of decks) {
  process.stdout.write(`\nBuilding TA ${deck} deck…\n`)
  const outputDirectory = fileURLToPath(
    new URL(`../../slides/ta/${deck}/`, import.meta.url),
  )
  rmSync(outputDirectory, { recursive: true, force: true })

  const result = spawnSync(
    './node_modules/.bin/slidev',
    [
      'build',
      `${deck}.md`,
      '--base',
      './',
      '--router-mode',
      'hash',
      '--out',
      `../../slides/ta/${deck}`,
    ],
    {
      cwd: workingDirectory,
      stdio: 'inherit',
    },
  )

  if (result.status !== 0)
    process.exit(result.status ?? 1)
}
