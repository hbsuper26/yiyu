from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))    
    page.on("pageerror", lambda exc: print(f"Page Error: {exc}"))

    page.goto("http://localhost:8081")
    page.wait_for_timeout(2000)
    page.screenshot(path="screenshot_top.png", full_page=True)
    browser.close()
