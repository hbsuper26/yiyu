from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    page.goto("http://localhost:8085/articles")
    page.wait_for_timeout(2000)
    page.screenshot(path="screenshot_articles.png")
    
    # Test clicking a tab
    page.click("text='官方公告'")
    page.wait_for_timeout(1000)
    page.screenshot(path="screenshot_articles_news.png")
    
    browser.close()
