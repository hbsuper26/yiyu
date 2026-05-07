from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("http://localhost:8081")
    page.wait_for_timeout(1000)
    
    # Get all text
    print(page.evaluate("document.body.innerText"))
    
    browser.close()
