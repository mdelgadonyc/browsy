import getpass
import re
from datetime import date
import time

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

    #page.get_by_role("link", name="Jobs", exact=True).click()
    #page.get_by_role("link", name=re.compile(js["JOBSEARCH"])).click()
    console(page,js)

def jobapply(page, js):
    today = date.today()
    current_date = today.strftime("%m/%d/%Y")
    job_title = page.get_by_role("heading >> nth=1").text_content()
    company = page.get_by_role("link >> nth=8").text_content().strip()     # and nth-12 too?
    # Split URL to attain and save the half before the "?"
    job_url = page.url.split('?')[0]

    if (input("Would you like to apply? ").lower() == 'yes'):
        print(f'{current_date},{job_title},{company},{job_url},"""Easy Apply""",LinkedIn, Applied,')
    else:
        page.go_back()
        return
    
    #page.get_by_text("Application submitted").click()
    if page.get_by_text("Application submitted").is_visible():
        print('*** detected application already submitted')
        page.go_back()
        return

    time.sleep(5)

    if page.get_by_role("button", name="Easy Apply").is_visible():
        print("*** detected an easy apply button")
        if (input("Would you like to apply? ").lower() == 'yes'):
            page.get_by_role("button", name="Easy Apply").click()
            time.sleep(2)
        else:
            return

    while (page.get_by_role("button", name="Submit application").is_visible() is not True):
        if page.get_by_label("City").is_visible():
            page.get_by_label("City").click()
            page.get_by_label("City").fill("new york")
            page.get_by_role("option", name="New York, New York, United States").locator("div").click()
            
        if page.get_by_role("button", name="Upload cover letter").is_visible():
            print("Optional cover letter detected")

        if page.get_by_role("combobox", name="Disability Status").is_visible():
            print("disability question detected")
            page.get_by_role("combobox", name="Disability Status").select_option("No, I don't have a disability, or a history/record of having a disability")

        if page.get_by_role("combobox", name="Veteran Status").is_visible():
            print("veteran status question detected")
            page.get_by_role("combobox", name="Veteran Status").select_option("I am not a protected veteran")

        if page.locator("#text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3536588865-6576016967321240801-multipleChoice").is_visible():
            print("race/ethnicity question detected")
            page.locator("#text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3536588865-6576016967321240801-multipleChoice").select_option("Hispanic or Latino")

        if page.get_by_role("combobox", name="Gender").is_visible():
            print("gender question detected")
            page.get_by_role("combobox", name="Gender").select_option("Male")

        for row in page.get_by_text(re.compile(r'How many years of .* experience do you have\?')).all():
            row.fill("3")
            print('*** answered the default "3" years to the question: ' + row.text_content().strip())

        if page.get_by_text(re.compile(r'Do you have .*\?')).is_visible():
            for row in page.get_by_text(re.compile(r'Do you have .*\?')).all():
                print('*** answered the default "3" to the question: ' + row.text_content().strip())
                row.select_option(label="Yes")

        if page.get_by_role("button", name="Continue to next step").is_visible():
            #if (input("continue with application? ").lower() == "yes"):
            time.sleep(3)
            page.get_by_role("button", name="Continue to next step").click()

        if page.get_by_role("button", name="Review your application").is_visible():
            #if (input("review your application? ").lower() == "yes"):
            time.sleep(3)
            page.get_by_role("button", name="Review your application").click()
        if page.get_by_text(re.compile(r'Follow \w+\s?\w* to stay up to date with their page.')).is_visible():
            #if (input("unclick follow? ").lower() == "yes"):
            print("*** detected a follow company checkbox. Unchecking...")
            time.sleep(2)
            page.get_by_text(re.compile(r'Follow \w+\s?\w* to stay up to date with their page.')).click()
            
        if page.get_by_role("button", name="Submit application").is_visible():
            if (input("*** detected the submit application button. do you wish to submit? ").lower() == "yes"):
                page.get_by_role("button", name="Submit application").click()
                time.sleep(2)
                break

def console(page, js):
    site_name = js["JOBSITE"]
    while (1):
        cmd = input(f'[{site_name}] --> ')
        if cmd == 'exit':
            break
        if cmd == 'dump':
            print(page.content())
        if cmd == 'apply':
            jobapply(page, js)
        if cmd == 'apply2':
            pass
            '''
            if page.get_by_role("button", name="Easy Apply").is_visible():
                print("*** detected an easy apply button")
                time.sleep(2)
                page.get_by_role("button", name="Easy Apply").click()
                time.sleep(2)
            jobapply(page, js)
            '''
