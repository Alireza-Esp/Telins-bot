"""Starter script for Tel-bot"""

import os
import json
import telebot
from telbot import Page

# Initializing project directory path
project_directory_path = input("Enter project directory path: ")
project_directory_path = os.path.abspath(project_directory_path)
print("\n")

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


@sender_bot.message_handler(commands=["start"])
def send_start(message: telebot.types.Message):
    """Implements /start command codes."""

    start_message = f"سلام {message.from_user.full_name} عزیز،\n"
    start_message += "به تلینس بات خوش اومدی.😊\n"
    start_message += "با ارسال دستور /signup جزو کاربرانی قرار میگیری که میتونن از پست ها و استوری های جدید پیج های زیر مطلع بشن:"
    for page in pages_list:
        start_message += f"\n{page.username}"

    sender_bot.send_message(message.chat.id, start_message)


@sender_bot.message_handler(commands=["signup"])
def send_signup(message: telebot.types.Message):
    """Implements /signup command codes."""

    if message.chat.id not in members_list:
        members_list.append(message.chat.id)
        json.dump({"members": members_list}, open(
            members_list_file_path, "w", encoding="utf-8"))
        signup_message = "به لیست کاربران اضافه شدی عزیزم.🙂"
        sender_bot.reply_to(message, signup_message)
    else:
        signup_message = "قبلا به لیست کاربران اضافه شدی عزیزم.😎"
        sender_bot.reply_to(message, signup_message)

    print(members_list)


sender_bot.infinity_polling()
