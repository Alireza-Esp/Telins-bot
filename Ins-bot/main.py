"""Main script for Ins-bot"""
import os
import json
import traceback
from time import sleep
from instagrapi import Client
from persiantools.jdatetime import JalaliDateTime
from insbot import Page, log_and_print, scrap


# Initializing project directory path
project_directory_path = input("Enter project directory path: ")
project_directory_path = os.path.abspath(project_directory_path)
print("\n")

# Creating "api" folder in choosen directory
if not os.path.exists(os.path.join(project_directory_path, "api")):
    os.mkdir(os.path.join(project_directory_path, "api"))

# Creating "api/stories" folder in choosen directory
if not os.path.exists(os.path.join(project_directory_path, "api/stories")):
    os.mkdir(os.path.join(
        project_directory_path, "api/stories"))

# Creating "api/posts" folder in choosen directory
if not os.path.exists(os.path.join(project_directory_path, "api/posts")):
    os.mkdir(os.path.join(
        project_directory_path, "api/posts"))

# Initializing TB_Activator_file_path in "api" folder and creating "TB-Activator" json file
TB_Activator_file_path = os.path.join(
    project_directory_path, "api/TB-Activator.json")
json.dump(
    {"active": False},
    open(TB_Activator_file_path, "w", encoding="utf-8")
)


# Creating log.txt file path
logsfile = open(os.path.join(project_directory_path,
                "logs.txt"), "a", encoding="utf-8")

# Reading datas from config.json
datas = json.load(
    open(os.path.join(project_directory_path, "config.json"), "r", encoding="utf-8")
)

# Initializing timeframe
time_frame = float(datas["time_frame"])

# Creating scraper bot instance and logining with
scrapper_bot = Client()
print("Trying to login...")
scrapper_bot.login(
    datas["insta_bot_info"]["username"],
    datas["insta_bot_info"]["password"]
)
print("Login done.")

# Creating instances for pages
page1 = Page(
    scarpper=scrapper_bot,
    username=datas["page1_info"]["username"],
    directory_path_to_save_datas=project_directory_path,
    jsons_files_name=datas["page1_info"]["jsons_files_name"])

if "page2_info" in list(datas.keys()):
    page2 = Page(
        scarpper=scrapper_bot,
        username=datas["page2_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page2_info"]["jsons_files_name"])
else:
    page2 = []

if "page3_info" in list(datas.keys()):
    page3 = Page(
        scarpper=scrapper_bot,
        username=datas["page3_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page3_info"]["jsons_files_name"])
else:
    page3 = []

if "page4_info" in list(datas.keys()):
    page4 = Page(
        scarpper=scrapper_bot,
        username=datas["page4_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page4_info"]["jsons_files_name"])
else:
    page4 = []

if "page5_info" in list(datas.keys()):
    page5 = Page(
        scarpper=scrapper_bot,
        username=datas["page5_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page5_info"]["jsons_files_name"])
else:
    page5 = []

if "page6_info" in list(datas.keys()):
    page6 = Page(
        scarpper=scrapper_bot,
        username=datas["page6_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page6_info"]["jsons_files_name"])
else:
    page6 = []

if "page7_info" in list(datas.keys()):
    page7 = Page(
        scarpper=scrapper_bot,
        username=datas["page7_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page7_info"]["jsons_files_name"])
else:
    page7 = []

if "page8_info" in list(datas.keys()):
    page8 = Page(
        scarpper=scrapper_bot,
        username=datas["page8_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page8_info"]["jsons_files_name"])
else:
    page8 = []

if "page9_info" in list(datas.keys()):
    page9 = Page(
        scarpper=scrapper_bot,
        username=datas["page9_info"]["username"],
        directory_path_to_save_datas=scrapper_bot,
        jsons_files_name=datas["page9_info"]["jsons_files_name"])
else:
    page9 = []

if "page10_info" in list(datas.keys()):
    page10 = Page(
        scarpper=scrapper_bot,
        username=datas["page10_info"]["username"],
        directory_path_to_save_datas=project_directory_path,
        jsons_files_name=datas["page10_info"]["jsons_files_name"])
else:
    page10 = []


# Adding pages in a list
pages_list = [
    page1,
    page2,
    page3,
    page4,
    page5,
    page6,
    page7,
    page8,
    page9,
    page10
]

for page in pages_list[:]:
    if page == []:
        pages_list.remove(page)

print("Initializing pages...")
# Initializing pages
for page in pages_list:
    page.first_initialize()

# Saving initial log in logs.txt
log_and_print(
    f"Enter project directory path: {project_directory_path}",
    logsfile,
    False
)
log_and_print(
    "Trying to login...\nLogin done.",
    logsfile,
    False
)
log_and_print("Recognized page(s):", logsfile)
for page in pages_list:
    log_and_print(f"  {page.username}", logsfile)

# Initializing PROID
PROID = 0


def main():
    # Globalling PROID cause it will be changed
    global PROID

    # Looping in main workflow
    while True:
        has_result = False
        if time_frame == 0.25:
            if JalaliDateTime.now().minute in [0, 15, 30, 45]:
                has_result = scrap(logsfile, PROID, pages_list)
                PROID += 1

        elif time_frame == 0.5:
            if JalaliDateTime.now().minute in [0, 30]:
                has_result = scrap(logsfile, PROID, pages_list)
                PROID += 1

        elif time_frame in [1, 2, 3, 4, 6, 8, 12, 24]:
            if (JalaliDateTime.now().hour % time_frame == 0) and (JalaliDateTime.now().minute == 0):
                has_result = scrap(logsfile, PROID, pages_list)
                PROID += 1

        # Setting "active" true if needed
        if has_result is True:
            json.dump(
                {"active": True},
                open(TB_Activator_file_path, "w", encoding="utf-8")
            )

        # Sleeping
        sleep(60)


try:
    main()
except Exception as error:
    # Logging and printing traceback in log.txt
    log_and_print("\n\n\n", logsfile)
    log_and_print("AN ERROR OCCURRED...", logsfile)
    for line in traceback.format_exception(error):
        log_and_print(line, logsfile)
