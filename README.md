# honeycombtheworldbeyond.wiki

Independent fan wiki for **Honeycomb: The World Beyond** (Steam AppID: 1510440)  
Developer: Frozen Way | Publisher: Snail Games USA | Release: September 8, 2026

## Site Structure

```
honeycombtheworldbeyond_wiki/
├── index.html              # Homepage — hero, gallery, FAQ, Steam CTA
├── guides.html             # Beginner survival guide (HowTo schema)
├── crossbreeding.html      # Grafting & Allogamy mechanic guide
├── biomes.html             # Sota7 biomes directory with biome cards
├── species.html            # Flora & fauna database with trait profiles
├── base-building.html      # Module priority guide & layout strategy
├── demo-guide.html         # Steam demo walkthrough (Aug 31 demo)
├── privacy.html            # Privacy policy (noindex)
├── styles.css              # VRE-driven design system (biopunk sci-fi)
├── favicon.svg             # Honeycomb hexagon SVG favicon
├── site.webmanifest        # PWA manifest
├── robots.txt              # Allow all, Sitemap pointer
├── sitemap.xml             # 8-page sitemap with image entry
├── ads.txt                 # AdSense placeholder
├── llms.txt                # LLM crawler permissions
├── steam_meta.json         # Cached Steam API metadata
├── opportunity.json        # Keyword opportunity contract (GO_NOW)
├── site-contract.json      # SEO audit checklist contract
├── EVIDENCE.md             # Source manifest with screenshot VRE table
└── assets/
    ├── steam_header.jpg    # Official key art (65KB)
    ├── screenshot_1.jpg    # Nighttime base camp (669KB)
    ├── screenshot_2.jpg    # River crossing biome (744KB)
    ├── screenshot_3.jpg    # Open meadow / watering hole (494KB)
    ├── screenshot_4.jpg    # Amber Plains scanning (723KB)
    ├── screenshot_5.jpg    # Fauna interaction (659KB)
    ├── screenshot_6.jpg    # Laboratory interior (586KB)
    ├── screenshot_7.jpg    # Underwater / Abyssal (442KB)
    └── screenshot_8.jpg    # Base building planning (675KB)
```

## Design System

Colors extracted via VRE (Visual Reverse-Engineering) from official Steam screenshots:
- `--color-bg: #091c18` — dark forest night
- `--color-brand: #4ecdc4` — HUD compass arc / health bar cyan  
- `--color-accent: #f7d060` — scanning tooltip amber
- `--color-bio: #8b5cf6` — alien tree violet
- `--color-nature: #4a9e5c` — Sota7 grass green

Game-native UI components in CSS: scan-tooltip (pill shape with amber bar), hud-stat bars (4 survival metrics), breed-diagram (parent→hybrid crossbreeding flow).

## Deployment Checklist

See `rules/skills/site-search-onboarding/SKILL.md` for full deployment workflow.

### Step 1: GitHub Repository
```bash
git init
git add -A
git commit -m "feat: initial honeycombtheworldbeyond.wiki"
git remote add origin https://github.com/YOUR_ORG/honeycombtheworldbeyond-wiki
git push -u origin main
```

### Step 2: Cloudflare Pages
- Go to Cloudflare Dashboard > Pages > Create Application
- Connect GitHub repo
- Build settings: Framework = "None", Build command = (empty), Output directory = "."
- Add custom domain: honeycombtheworldbeyond.wiki

### Step 3: Domain DNS (if not auto-configured)
- Spaceship / registrar: Add CNAME record
  - `honeycombtheworldbeyond.wiki` → `your-project.pages.dev`
- See `rules/skills/domain-dns-onboarding/SKILL.md`

### Step 4: Google Search Console
- Go to https://search.google.com/search-console/
- Add property: `https://honeycombtheworldbeyond.wiki/`
- Verify via HTML file (rename `google-site-verification-placeholder.html`)
- Submit sitemap: `https://honeycombtheworldbeyond.wiki/sitemap.xml`

### Step 5: Bing Webmaster Tools
- Note: Bing SOAP Ping API retired August 31, 2026
- Submit via: https://www.bing.com/webmasters/ → Add site → sitemap URL
- Verify via DNS TXT or HTML file method

### Step 6: Google AdSense
- See `rules/skills/adsense-site-onboarding/SKILL.md`
- Apply at: https://www.google.com/adsense/
- Update `ads.txt` with your publisher ID: `pub-XXXXXXXXXXXXXXXXX`
- AdSense requires site to be live and indexed first

## Content Update Plan (Post-Launch)

After September 8, 2026:
- [ ] Update species database with confirmed in-game names
- [ ] Add crossbreeding compatibility matrix from in-game data
- [ ] Verify biome names and add sub-biome entries
- [ ] Add EON Corp mission guide
- [ ] Add patch notes tracker
