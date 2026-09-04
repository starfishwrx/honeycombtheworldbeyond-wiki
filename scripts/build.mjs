import { rm, mkdir, cp } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = resolve(root, 'dist');

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

const files = [
  'index.html', 'guides.html', 'crossbreeding.html', 'biomes.html',
  'species.html', 'base-building.html', 'demo-guide.html', 'privacy.html',
  '404.html', 'styles.css', 'robots.txt', 'sitemap.xml', 'llms.txt',
  'ads.txt', 'favicon.ico', 'favicon.svg', 'icon-48.png', 'icon-192.png',
  'apple-touch-icon.png', 'site.webmanifest', 'CNAME',
  '_headers', '_redirects', 'site-contract.json', 'opportunity.json',
  'launch-profile.json', 'launch-report.json', 'EVIDENCE.md', 'wrangler.jsonc'
];

for (const file of files) {
  try {
    await cp(resolve(root, file), resolve(dist, file));
  } catch {
    // ignore missing optional files
  }
}

try {
  await cp(resolve(root, 'assets'), resolve(dist, 'assets'), { recursive: true });
} catch {
  // ignore
}

console.log('[SUCCESS] Production bundle compiled to:', dist);
