#!/usr/bin/env python3
"""Idempotently inject GA4 tracking script with basic consent mode into wiki HTML pages."""
import os
import re
import sys
from pathlib import Path

DEFAULT_ID = "G-03MXLX12W1"

def get_measurement_id() -> str:
    return os.environ.get("GA_MEASUREMENT_ID") or DEFAULT_ID

def make_snippet(mid: str) -> str:
    return f"""  <!-- Google Analytics 4 (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={mid}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('consent', 'default', {{
      'analytics_storage': 'granted'
    }});
    gtag('config', '{mid}', {{
      'anonymize_ip': true
    }});
  </script>"""

PAGES = [
    "index.html", "guides.html", "crossbreeding.html", "biomes.html",
    "species.html", "base-building.html", "demo-guide.html", "privacy.html",
    "404.html"
]

def inject(root: Path, mid: str) -> int:
    snippet = make_snippet(mid)
    changed = 0
    for name in PAGES:
        p = root / name
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        if f"gtag/js?id={mid}" in html:
            continue
        if "gtag/js?id=" in html:
            # Replace existing GA4 block
            html = re.sub(r"\s*<!-- Google Analytics 4 \(GA4\) -->[\s\S]*?</script>\s*</script>", "", html)
            html = re.sub(r"\s*<script async src=\"https://www.googletagmanager.com/gtag/js[\s\S]*?</script>\s*</script>", "", html)
        if "</head>" in html:
            html = html.replace("</head>", f"{snippet}\n</head>")
            p.write_text(html, encoding="utf-8")
            print(f"Injected GA4 ({mid}) into {name}")
            changed += 1
    return changed

def remove(root: Path) -> int:
    changed = 0
    for name in PAGES:
        p = root / name
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        if "<!-- Google Analytics 4 (GA4) -->" in html:
            html = re.sub(r"\s*<!-- Google Analytics 4 \(GA4\) -->[\s\S]*?</script>\s*</script>", "", html)
            p.write_text(html, encoding="utf-8")
            print(f"Removed GA4 from {name}")
            changed += 1
    return changed

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    if "--remove" in sys.argv:
        count = remove(root)
        print(f"Removed GA4 from {count} pages.")
    else:
        mid = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else get_measurement_id()
        count = inject(root, mid)
        print(f"Done. Injected {count} pages.")
