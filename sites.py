import getpass
import re

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

    page.get_by_role("link", name="Jobs").click()
    page.get_by_role("link", name=re.compile(js["JOBSEARCH"])).click()


    while (1):
        cmd = input(f'[{js["JOBSITE"]}] --> ')
        if cmd == 'exit':
            break
        if cmd == 'dump':
            print(page.content())
        if cmd == 'apply':
            print(page.locator(f'xpath={js["JOBXPATH"]}').text_content())
            page.locator(f'xpath={js["JOBXPATH"]}').click()
        