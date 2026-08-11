import { readFile, writeFile } from 'node:fs/promises'
import { resolve } from 'node:path'

const sitemapPath = resolve('_site/sitemap.xml')
const unlistedPaths = [
  '/ta/index.html',
  '/9065_tut_01.html',
]

let sitemap
try {
  sitemap = await readFile(sitemapPath, 'utf8')
}
catch (error) {
  if (error?.code === 'ENOENT')
    process.exit(0)
  throw error
}

let removed = 0
const filtered = sitemap.replace(/  <url>\n[\s\S]*?  <\/url>\n/g, (entry) => {
  if (!unlistedPaths.some(path => entry.includes(path)))
    return entry
  removed += 1
  return ''
})

if (removed > 0) {
  await writeFile(sitemapPath, filtered)
  process.stdout.write(`Removed ${removed} unlisted sitemap entries.\n`)
}
