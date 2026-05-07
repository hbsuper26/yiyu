from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
    page.on("pageerror", lambda exc: print(f"Page Error: {exc}"))
    
    file_url = f"file:///{os.path.abspath('test_alpine.html').replace(chr(92), '/')}"
    page.goto(file_url)
    page.wait_for_timeout(1000)
    
    print("Test1 text:", page.evaluate("document.getElementById('test1').innerText"))
    print("Test2 text:", page.evaluate("document.getElementById('test2').innerText"))
    browser.close()
