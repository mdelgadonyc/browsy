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
    print(f'Data from file: {js}')
    print(f'job site name: {js["JOBSITE"]}')

    chromium_dir = Path.home() / '.config/chromium'
    print(f'chromium_dir is: {chromium_dir}')
    browser = playwright.chromium.launch_persistent_context(chromium_dir, headless=False)
    page = browser.new_page()
    page.goto( js["$HOME_PAGE"] )
    page.get_by_role("combobox", name="Search").click()
    page.get_by_role("combobox", name="Search").fill("Hello world!")
    page.get_by_role("combobox", name="Search").press("Enter")

    # uncomment line below to skip to jobsite for debugging purposes
    # sites.jobsite(page, js)

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
        if cmd == js["JOBSITE"]:
            sites.jobsite(page, js)
        if cmd == js["WORK"]["WORKSITE"]:
            sites.worksite(page, js)

prog_name = sys.argv[0]

if len(sys.argv) != 2:
    print(f"usage: {prog_name} <dictionary file>")
    exit()

with sync_playwright() as playwright:
    run(playwright, sys.argv[1])
