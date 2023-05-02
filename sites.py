import getpass
import re
from datetime import date

site_name = ''

def worksite(page, js):
    page.goto(js["WORK"]["WORKURL"])
    if ((page.get_by_placeholder("UNI")).is_visible()):
        print("authentication necessary")
        secret = getpass.getpass()
        page.get_by_placeholder("UNI").click()
        page.get_by_placeholder("UNI").fill(js["WORK"]["USERNAME"])
        page.get_by_placeholder("UNI").press("Tab")
        page.get_by_placeholder("Password").fill(secret)
        page.get_by_placeholder("Password").press("Enter")
        page.frame_locator("#duo_iframe").get_by_role("button", name="Send Me a Push").click()

    console(page, js)

def jobsite(page, js):

    page.goto(js["JOBURL"])

# add code to skip if already signed in
#    page.get_by_role("link", name="Sign in").click()
#    page.get_by_label("Email or Phone").click()
#    page.get_by_label("Email or Phone").fill(js["JOBURL"])
#    page.get_by_label("Password").click()
#    secret = getpass.getpass()
#    page.get_by_label("Password").fill({secret})
#    page.get_by_role("button", name="Sign in", exact=True).click()

    page.get_by_role("link", name="Jobs", exact=True).click()
    page.get_by_role("link", name=re.compile(js["JOBSEARCH"])).click()
    console(page,js)

def console(page, js):
    site_name = 'js["JOBSITE"]'
    while (1):
        cmd = input(f'[{site_name}] --> ')
        if cmd == 'exit':
            break
        if cmd == 'dump':
            print(page.content())
        if cmd == 'apply':
            today = date.today()
            current_date = today.strftime("%m/%d/%Y")
            job_title = page.locator(f'xpath={js["JOBXPATH"]}').text_content().strip()
            company = page.locator(f'xpath={js["CORPPATH"]}').text_content().strip()
            page.locator(f'xpath={js["JOBXPATH"]}').click()
            # Split URL to attain and save the half before the "?"
            job_url = page.url.split('?')
            print(f'{current_date},{job_title},{company},{job_url[0]}')
            page.get_by_role("button", name="Apply").click()