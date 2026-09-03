import shutil
from pathlib import Path

def build():
    root = Path(__file__).parent.resolve()
    dist = root / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True)

    # Core files to copy
    files = [
        'index.html', 'guides.html', 'crossbreeding.html', 'biomes.html',
        'species.html', 'base-building.html', 'demo-guide.html', 'privacy.html',
        '404.html', 'styles.css', 'robots.txt', 'sitemap.xml', 'llms.txt',
        'ads.txt', 'favicon.ico', 'favicon.svg', 'icon-48.png', 'icon-192.png',
        'apple-touch-icon.png', 'site.webmanifest', 'CNAME',
        '_headers', '_redirects', 'site-contract.json', 'opportunity.json',
        'launch-profile.json', 'launch-report.json', 'EVIDENCE.md'
    ]

    for item in files:
        src = root / item
        if src.exists():
            shutil.copy2(src, dist / item)

    # Assets folder
    if (root / 'assets').exists():
        shutil.copytree(root / 'assets', dist / 'assets')

    print(f"[SUCCESS] Production bundle compiled to: {dist}")

if __name__ == '__main__':
    build()
