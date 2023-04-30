import json
import sys
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright, dictionary) -> None:

    # Read dictionary from file
    with open(dictionary) as file:
        data = file.read()

    js = json.loads(data)

    print(f'Data from file: {data}')
    print(f'Data after json.loads: {js}')
    
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
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


prog_name = sys.argv[0]

if len(sys.argv) != 2:
    print(f"usage: {prog_name} <dictionary file>")
    exit()

with sync_playwright() as playwright:
    run(playwright, sys.argv[1])
