import re
from pathlib import Path

def update_pages():
    root = Path(__file__).parents[1]
    html_files = list(root.glob("*.html"))

    nav_script_replacement = """<script>
// Mobile nav toggle & auto-close on link click
const hamburger = document.querySelector('.nav-hamburger');
const navLinks = document.querySelector('.nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  navLinks.addEventListener('click', (e) => {
    if (e.target.closest('a')) {
      navLinks.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });
}
"""

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        
        # 1. Update stylesheet reference to versioned cache-busting
        text = re.sub(r'href="styles\.css(?:\?v=[^"]*)?"', 'href="styles.css?v=20260903-1"', text)
        
        # 2. Update nav toggle script if present
        if "// Mobile nav toggle" in text:
            text = re.sub(
                r'// Mobile nav toggle[\s\S]*?document\.querySelector\(\'\.nav-links\'\)\?\.classList\.toggle\(\'open\'\);\s*\}\);',
                """// Mobile nav toggle & auto-close on link click
const hamburger = document.querySelector('.nav-hamburger');
const navLinks = document.querySelector('.nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  navLinks.addEventListener('click', (e) => {
    if (e.target.closest('a')) {
      navLinks.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });
}""",
                text
            )
        elif "</body>" in text and "<nav class=\"nav-bar\">" in text:
            # Inject script before </body>
            text = text.replace("</body>", f"{nav_script_replacement}</script>\n</body>")

        # 3. Add aria-expanded="false" to hamburger if missing
        text = re.sub(
            r'<button class="nav-hamburger" aria-label="Menu">',
            '<button class="nav-hamburger" aria-label="Menu" aria-expanded="false">',
            text
        )

        path.write_text(text, encoding="utf-8")
        print(f"[OK] Updated {path.name}")

if __name__ == "__main__":
    update_pages()
