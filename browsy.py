import json
import sys
import logging
from playwright.sync_api import Playwright, sync_playwright, expect
from pathlib import Path


def run(playwright: Playwright, dictionary) -> None:
    # Switch from DEBUG to CRITICAL to reduce verbosity
    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger()

    # Read dictionary from file
    with open(dictionary) as file:
        data = file.read()

    js = json.loads(data)

    logging.debug(f'Data from file: {js}')

    chromium_dir = Path.home() / '.config/chromium'
    logging.debug(f'chromium_dir is: {chromium_dir}')
    browser = playwright.chromium.launch_persistent_context(chromium_dir, headless=False)

    page = browser.new_page()
    page.goto(js["$HOME_PAGE"])

    # TODO: Add "Browsy" ASCII logo

    print("Use command 'help' for list of available commands")
    while 1:
        cmd = input("--> ")
        if cmd == 'help':
            print("available commands: dump, exit, goto, help, simple")
        if cmd == 'exit':
            exit()
        if cmd == 'simple':
            page.goto("https://phet-dev.colorado.edu/html/build-an-atom/0.0.0-3/simple-text-only-test-page.html")
        if cmd == 'dump':
            print(page.content())
        if cmd == 'goto':
            url = input("URL: ")
            # append https:// to start of URL if not provided.
            if not url.startswith("http"):
                url = f"https://{url}"
            page.goto(url)


prog_name = sys.argv[0]

if len(sys.argv) != 2:
    print(f"usage: {prog_name} <dictionary file>")
    exit()

with sync_playwright() as playwright:
    run(playwright, sys.argv[1])

# TODO - Add ASCII intro text
