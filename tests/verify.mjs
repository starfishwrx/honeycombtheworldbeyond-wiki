import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const files = [];

async function walk(dir) {
  for (const name of await readdir(dir)) {
    const p = join(dir, name);
    const s = await stat(p);
    if (s.isDirectory()) {
      if (!['node_modules', '.git', 'tmp'].includes(name)) await walk(p);
    } else {
      files.push(p);
    }
  }
}

await walk(root);
const rel = files.map(f => relative(root, f).replaceAll('\\', '/'));

const indexablePages = [
  'index.html',
  'guides.html',
  'crossbreeding.html',
  'biomes.html',
  'species.html',
  'base-building.html',
  'demo-guide.html',
  'privacy.html'
];

const requiredFiles = [
  ...indexablePages,
  'styles.css',
  'robots.txt',
  'sitemap.xml',
  'ads.txt',
  'llms.txt',
  'site.webmanifest',
  'favicon.svg',
  'favicon.ico',
  'icon-48.png',
  'icon-192.png',
  'apple-touch-icon.png',
  'CNAME',
  'steam_meta.json',
  'opportunity.json',
  'site-contract.json',
  'launch-profile.json',
  'launch-report.json',
  'EVIDENCE.md',
  'assets/steam_header.jpg',
  'assets/screenshot_1.jpg',
  'assets/screenshot_2.jpg',
  'assets/screenshot_3.jpg',
  'assets/screenshot_4.jpg',
  'assets/screenshot_5.jpg',
  'assets/screenshot_6.jpg',
  'assets/screenshot_7.jpg',
  'assets/screenshot_8.jpg'
];

for (const f of requiredFiles) {
  if (!rel.includes(f)) {
    throw new Error(`Missing required file: ${f}`);
  }
}

for (const page of indexablePages) {
  const content = await readFile(join(root, page), 'utf8');
  for (const token of ['<title>', '<meta name="description"', '<link rel="canonical"', 'styles.css', 'site-footer', 'nav-bar']) {
    if (!content.includes(token)) {
      throw new Error(`${token} missing in ${page}`);
    }
  }

  // Verify internal links
  const matches = content.matchAll(/href="([^"#:]+)"/g);
  for (const m of matches) {
    const href = m[1];
    if (href === '/' || href.startsWith('http') || href.startsWith('mailto:')) continue;
    const cleanHref = href.split('?')[0].replace(/^\//, '');
    if (!cleanHref) continue;
    if (!rel.includes(cleanHref)) {
      throw new Error(`Broken internal link in ${page}: ${cleanHref}`);
    }
  }

  // Verify image sources (excluding inline JS template strings)
  const htmlWithoutScripts = content.replace(/<script[\s\S]*?<\/script>/gi, '');
  const imgMatches = htmlWithoutScripts.matchAll(/src="([^":]+)"/g);
  for (const m of imgMatches) {
    const src = m[1];
    if (src.startsWith('http') || src.startsWith('data:')) continue;
    const cleanSrc = src.split('?')[0].replace(/^\//, '');
    if (!rel.includes(cleanSrc)) {
      throw new Error(`Broken local image reference in ${page}: ${cleanSrc}`);
    }
  }
}

// Check sitemap contains all indexable pages
const sitemap = await readFile(join(root, 'sitemap.xml'), 'utf8');
for (const p of indexablePages) {
  const target = p === 'index.html' ? 'https://honeycombtheworldbeyond.wiki/' : `https://honeycombtheworldbeyond.wiki/${p}`;
  if (!sitemap.includes(target)) {
    throw new Error(`sitemap.xml missing URL: ${target}`);
  }
}

// Check CNAME content
const cname = (await readFile(join(root, 'CNAME'), 'utf8')).trim();
if (cname !== 'honeycombtheworldbeyond.wiki') {
  throw new Error(`CNAME expected 'honeycombtheworldbeyond.wiki', got: '${cname}'`);
}

console.log(`PASS: All ${indexablePages.length} pages verified; all ${requiredFiles.length} required assets & contracts present; sitemap and CNAME valid.`);
