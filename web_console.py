import json
import sys
from playwright.sync_api import Playwright, sync_playwright, expect
from pathlib import Path
import bwfun
import sites 

def run(playwright: Playwright, dictionary) -> None:

    # Read dictionary from file
    with open(dictionary) as file:
        data = file.read()

    js = json.loads(data)

    print(f'Data from file: {data}')
    print(f'Data after json.loads: {js}')
    
    chromium_dir = Path.home() / '.config/chromium'
    print(f'chromium_dir is: {chromium_dir}')
    #browser = playwright.chromium.launch(headless=False)   # doesn't persist session
    browser = playwright.chromium.launch_persistent_context(chromium_dir, headless=False)
    page = browser.new_page()
    page.goto( js["$HOME_PAGE"] )
    page.get_by_role("combobox", name="Search").click()
    page.get_by_role("combobox", name="Search").fill("Hello world!")
    page.get_by_role("combobox", name="Search").press("Enter")

    while (1):
        cmd = input("--> ")
        if cmd == 'exit':
            exit()
        if cmd == 'youtube':
            page.goto("https://www.youtube.com/")
        if cmd == 'simple':
            page.goto("https://phet-dev.colorado.edu/html/build-an-atom/0.0.0-3/simple-text-only-test-page.html")
        if cmd == 'bwlogin':
            bwfun.bwlogin()
        if cmd == 'dump':
            print(page.content())
        if cmd == 'linkedin':
            sites.linkedin(page)

prog_name = sys.argv[0]

if len(sys.argv) != 2:
    print(f"usage: {prog_name} <dictionary file>")
    exit()

with sync_playwright() as playwright:
    run(playwright, sys.argv[1])
