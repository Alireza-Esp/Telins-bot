"""Main script for Tel-bot"""

import os
import json
# import traceback
import telebot
import telebot.types
from time import sleep
from telbot import Page

# Initializing project directory path
project_directory_path = input("Enter project directory path: ")
project_directory_path = os.path.abspath(project_directory_path)
print("\n")

# Initializing TB_Activator_file_path in "api" folder and active var
TB_Activator_file_path = os.path.join(
    project_directory_path, "api/TB-Activator.json")
active = json.load(open(TB_Activator_file_path,
                   "r", encoding="utf-8"))["active"]

# Reading datas from config.json
datas = json.load(
    open(os.path.join(project_directory_path, "config.json"), "r", encoding="utf-8")
)

# Creating sender bot instance
TOKEN = datas["tel_bot_info"]["token"]
sender_bot = telebot.TeleBot(TOKEN)

# Creating instances for pages
page1 = Page(
    sender=sender_bot,
    username=datas["page1_info"]["username"],
    directory_path_to_load_datas=project_directory_path,
    jsons_files_name=datas["page1_info"]["jsons_files_name"])

if "page2_info" in list(datas.keys()):
    page2 = Page(
        sender=sender_bot,
        username=datas["page2_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page2_info"]["jsons_files_name"])
else:
    page2 = []

if "page3_info" in list(datas.keys()):
    page3 = Page(
        sender=sender_bot,
        username=datas["page3_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page3_info"]["jsons_files_name"])
else:
    page3 = []

if "page4_info" in list(datas.keys()):
    page4 = Page(
        sender=sender_bot,
        username=datas["page4_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page4_info"]["jsons_files_name"])
else:
    page4 = []

if "page5_info" in list(datas.keys()):
    page5 = Page(
        sender=sender_bot,
        username=datas["page5_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page5_info"]["jsons_files_name"])
else:
    page5 = []

if "page6_info" in list(datas.keys()):
    page6 = Page(
        sender=sender_bot,
        username=datas["page6_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page6_info"]["jsons_files_name"])
else:
    page6 = []

if "page7_info" in list(datas.keys()):
    page7 = Page(
        sender=sender_bot,
        username=datas["page7_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page7_info"]["jsons_files_name"])
else:
    page7 = []

if "page8_info" in list(datas.keys()):
    page8 = Page(
        sender=sender_bot,
        username=datas["page8_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page8_info"]["jsons_files_name"])
else:
    page8 = []

if "page9_info" in list(datas.keys()):
    page9 = Page(
        sender=sender_bot,
        username=datas["page9_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
        jsons_files_name=datas["page9_info"]["jsons_files_name"])
else:
    page9 = []

if "page10_info" in list(datas.keys()):
    page10 = Page(
        sender=sender_bot,
        username=datas["page10_info"]["username"],
        directory_path_to_load_datas=project_directory_path,
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

# Initializing members list
members_list = []

# Initializing members_list_file_path
members_list_file_path = os.path.join(
    project_directory_path, "api/Members-List.json")


def main():
    """Main function of program"""
    # Looping in main workflow
    while True:
        # Updating "active" var status from TB_Activator_file_path
        active = json.load(open(TB_Activator_file_path,
                                "r", encoding="utf-8"))["active"]

        if active is True:
            # Upadating "members_list" from members_list_file_path
            members_list = json.load(
                open(members_list_file_path, "r", encoding="utf-8")
            )["members"]

            # Showing getting infos from server
            for member in members_list:
                sender_bot.send_message(
                    member, "در حال دریافت اطلاعات از سرور...")

            # Getting stories, single posts and multiple posts for any page
            for page in pages_list:
                stories = page.get_new_stories()
                single_posts = page.get_new_single_posts()
                multiple_posts = page.get_new_multpile_posts()

                if (stories != {}) or (single_posts != {}) or (multiple_posts != {}):
                    for member in members_list:
                        sender_bot.send_message(
                            member, f"🔴 پیج : {page.username}")

                # Sending stories if exists
                if stories != {}:
                    for member in members_list:
                        sender_bot.send_message(member, "استوری ها :")

                    stories = zip(stories["types"], stories["links"])

                    for story in stories:
                        if story[0] == "photo":
                            for member in members_list:
                                sender_bot.send_photo(member, story[1])
                        elif story[0] == "video":
                            for member in members_list:
                                sender_bot.send_video(member, story[1])

                # Sending posts if exists
                if (single_posts != {}) or (multiple_posts != {}):
                    for member in members_list:
                        sender_bot.send_message(member, "پست ها :")

                # Single posts if exists
                if single_posts != {}:
                    single_posts = zip(
                        single_posts["types"],
                        single_posts["captions"],
                        single_posts["links"]
                    )

                for single_post in single_posts:
                    if single_post[0] == "photo":
                        for member in members_list:
                            sender_bot.send_photo(
                                member, single_post[2], caption=single_post[1])
                    elif single_post[0] in ["video", "igtv", "reel"]:
                        for member in members_list:
                            sender_bot.send_video(
                                member, single_post[2], caption=single_post[1])

                # Multiple posts if exists
                if multiple_posts != {}:
                    multiple_posts = zip(
                        multiple_posts["captions"],
                        multiple_posts["medias"]
                    )

                medias = []
                for multiple_post in multiple_posts:
                    # print(multiple_post)
                    # print(multiple_post[1].keys())
                    for key in list(multiple_post[1].keys()):
                        # print(key)
                        if multiple_post[1][key]["type"] == "photo":
                            medias.append(
                                telebot.types.InputMediaPhoto(
                                    multiple_post[1][key]["media_link"])
                            )
                        elif multiple_post[1][key]["type"] == "video":
                            medias.append(
                                telebot.types.InputMediaVideo(
                                    multiple_post[1][key]["media_link"])
                            )
                    for member in members_list:
                        messages_id = sender_bot.send_media_group(
                            member, medias)
                        sender_bot.reply_to(messages_id[0], multiple_post[0])

            json.dump({"active": False}, open(
                TB_Activator_file_path, "w", encoding="utf-8"))

        sleep(60)


main()
