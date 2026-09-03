import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def capture_renders():
    root = Path(__file__).parent.resolve()
    html_file = f"file:///{root.as_posix()}/index.html"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop 1440px
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(html_file, wait_until="networkidle")
        desktop_path = root / "desktop_render.png"
        await page.screenshot(path=str(desktop_path), full_page=True)
        print(f"[OK] Captured desktop render: {desktop_path}")
        
        # 2. Mobile 390px
        mobile_page = await browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        await mobile_page.goto(html_file, wait_until="networkidle")
        mobile_path = root / "mobile_render.png"
        await mobile_page.screenshot(path=str(mobile_path), full_page=True)
        print(f"[OK] Captured mobile render: {mobile_path}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_renders())
