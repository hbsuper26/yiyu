from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    page.goto("http://localhost:8081")
    page.wait_for_timeout(2000)
    
    # Check if elements have 'active' class
    reveals = page.evaluate("() => Array.from(document.querySelectorAll('.reveal')).map(el => el.className)")
    print("Reveal classes:", reveals)
    
    # Scroll down to trigger intersection observer
    page.evaluate("window.scrollBy(0, 1000)")
    page.wait_for_timeout(1000)
    reveals = page.evaluate("() => Array.from(document.querySelectorAll('.reveal')).map(el => el.className)")
    print("After scroll 1000:", reveals)

    page.evaluate("window.scrollBy(0, 1000)")
    page.wait_for_timeout(1000)
    reveals = page.evaluate("() => Array.from(document.querySelectorAll('.reveal')).map(el => el.className)")
    print("After scroll 2000:", reveals)
    
    browser.close()
