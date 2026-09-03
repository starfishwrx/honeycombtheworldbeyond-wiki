import { readdir, stat } from 'node:fs/promises';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(root, 'dist');
const files = [];

async function walk(dir) {
  for (const name of await readdir(dir)) {
    const path = join(dir, name);
    const info = await stat(path);
    if (info.isDirectory()) await walk(path);
    else files.push(relative(dist, path).replaceAll('\\', '/'));
  }
}

await walk(dist);

for (const required of ['index.html', '404.html', 'robots.txt', 'sitemap.xml', 'ads.txt', 'assets/steam_header.jpg']) {
  if (!files.includes(required)) throw new Error(`Production bundle missing: ${required}`);
}

for (const forbidden of [
  'CNAME',
  'EVIDENCE.md',
  'launch-profile.json',
  'launch-report.json',
  'opportunity.json',
  'site-contract.json',
  'wrangler.jsonc',
]) {
  if (files.includes(forbidden)) throw new Error(`Source-only file leaked into production bundle: ${forbidden}`);
}

console.log(`PASS: Production bundle contains ${files.length} public files and excludes source-only contracts/reports.`);
