import json
import sys
import logging
from playwright.sync_api import Playwright, sync_playwright, expect
from pathlib import Path
import sites


def run(playwright: Playwright, dictionary) -> None:
    # Switch from DEBUG to CRITICAL to reduce verbosity
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger()

    # Read dictionary from file
    with open(dictionary) as file:
        data = file.read()

    js = json.loads(data)

    logging.debug(f'Data from file: {js}')
    logging.debug(f'job site name: {js["JOBSITE"]}')

    chromium_dir = Path.home() / '.config/chromium'
    logging.debug(f'chromium_dir is: {chromium_dir}')
    browser = playwright.chromium.launch_persistent_context(chromium_dir, headless=False)

    page = browser.new_page()

    # uncomment either line below to skip to jobsearch or worksite for debugging purposes
    # sites.jobsearch(page, js)
    # sites.worksite(page, js, browser)

    while 1:
        cmd = input("--> ")
        if cmd == 'exit':
            exit()
        if cmd == 'simple':
            page.goto("https://phet-dev.colorado.edu/html/build-an-atom/0.0.0-3/simple-text-only-test-page.html")
        if cmd == 'dump':
            print(page.content())
        if cmd == js["JOBSEARCH"]:
            sites.jobsearch(page, js)
        if cmd == js["WORK"]["WORKSITE"]:
            sites.worksite(page, js, browser)


prog_name = sys.argv[0]

if len(sys.argv) != 2:
    print(f"usage: {prog_name} <dictionary file>")
    exit()

with sync_playwright() as playwright:
    run(playwright, sys.argv[1])
