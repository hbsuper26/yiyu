from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("http://localhost:8081")
    page.wait_for_timeout(1000)
    
    # Scroll down repeatedly
    for i in range(5):
        page.evaluate("window.scrollBy(0, 800)")
        page.wait_for_timeout(500)
        
    reveals = page.evaluate("() => Array.from(document.querySelectorAll('.reveal, .reveal-left, .reveal-right')).map(el => el.className)")
    for r in reveals:
        if 'active' not in r:
            print("NOT ACTIVE:", r)
            
    browser.close()
