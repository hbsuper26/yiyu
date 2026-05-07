from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    page.goto("http://localhost:8081")
    page.wait_for_timeout(2000)
    
    # Simulate mouse movement to trigger parallax and canvas
    page.mouse.move(100, 100)
    page.wait_for_timeout(100)
    page.mouse.move(400, 400)
    page.wait_for_timeout(100)
    page.mouse.move(800, 300)
    page.wait_for_timeout(500)
    
    page.screenshot(path="screenshot_hero_animated.png")
    browser.close()
