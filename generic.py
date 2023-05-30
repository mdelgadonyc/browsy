import time
import re
import logging

logger = logging.getLogger(__name__)


def tcit_generic(page, js, dictionary):

    uni = input("enter person's uni: ")

    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Caller", exact=True).fill(uni)
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Caller", exact=True).press("Tab")
    
    # For debugging
    for row in page.frame_locator("iframe[name=\"gsft_main\"]").get_by_role("combobox").all():
        logger.debug(row.text_content())

    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_role("combobox", name="Mandatory - preloaded with saved dataCategory").select_option(dictionary["CATEGORY"])
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_role("combobox", name="Subcategory").select_option(dictionary["SUBCATEGORY"])
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_role("combobox", name="Channel").select_option("walk-in")
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Affected CI", exact=True).fill(dictionary["AFFECTEDCI"])
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Caller", exact=True).press("Tab")
    
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Assignment group", exact=True).fill("serv")
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_role("option", name="Service Desk").click()
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Assigned to", exact=True).click()
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_role("cell", name=js["WORK"]["MYLASTNAME"]).click()

    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Short Description").fill(dictionary["SHORTDESC"])

    logger.debug("Caller name? " + page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Caller", exact=True).input_value())

    full_name = page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Caller", exact=True).input_value()
    time.sleep(1)

    # Check if specialized comment exist otherwise default to GLAD2ASSIST
    if "COMMENT" in dictionary:
        #comments = dictionary["COMMENT"]
        comments = "".join(dictionary["COMMENT"])
        comments = comments.replace("NAME", full_name.split()[0])
        logger.debug(f'comments: {comments}')
    else:
        action = dictionary["ACTION"]
        comments = js["WORK"]["GLAD2ASSIST"]
        comments = comments.replace("NAME", full_name.split()[0])
        comments = comments.replace("ACTION", action)

    # Check if specialized internal work note exist otherwise default to INOTE
    if "IACTION" in dictionary:
        internal = dictionary["IACTION"]
        internal = internal.replace("NAME", full_name)
    else:
        internal = js["WORK"]["INOTE"]
        internal = internal.replace("NAME", full_name)
        internal = internal.replace("ACTION", action)

    logger.debug(f'comments is: {comments} and internal is: {internal}')

    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Additional comments (Customer visible)", exact=True).fill(comments)
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Internal work notes", exact=True).click()
    page.frame_locator("iframe[name=\"gsft_main\"]").get_by_label("Internal work notes", exact=True).fill(internal)
