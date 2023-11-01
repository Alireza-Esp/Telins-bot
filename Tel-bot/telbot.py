"""Pages class"""
import os
import json
from telebot import TeleBot


class Page():
    """Class for pages"""
    def __init__(
        self,
        sender: TeleBot,
        username: str,
        directory_path_to_load_datas: str,
        jsons_files_name: str
    ):
        # Globalling page username
        self.username = username

        # Globalling sender bot
        self.sender = sender

        # Initializing and globalling stories api(json file)
        self.stories_json_file_path = os.path.join(
            directory_path_to_load_datas, f"api/stories/{jsons_files_name}.json"
        )

        # Initializing and globalling posts api(jsons file)
        self.single_posts_json_file_path = os.path.join(
            directory_path_to_load_datas, f"api/posts/{jsons_files_name}-single.json"
        )
        self.multiple_posts_json_file_path = os.path.join(
            directory_path_to_load_datas, f"api/posts/{jsons_files_name}-multiple.json"
        )

    def get_new_stories(self):
        """Gets new stories info from json file.

        Returns:
            dict: new stories dict with this algorithm:
                                                {
                                                    "types": TYPES(as list),
                                                    "links": LINKS(as list)
                                                }
        """
        contents = json.load(
            open(self.stories_json_file_path, "r", encoding="utf-8"))
        return contents

    def get_new_single_posts(self):
        """Gets new single posts info from json file.

        Returns:
            dict: new single post dict with this algorithm:
                                                {
                                                    "types": TYPES(as list),
                                                    "captions": CAPTIONS(as list),
                                                    "links": LINKS(as list)
                                                }
        """
        contents = json.load(
            open(self.single_posts_json_file_path, "r", encoding="utf-8"))
        return contents

    def get_new_multpile_posts(self):
        """Gets new multiple posts info from json file.

        Returns:
            dict: new multiple post dict with this algorithm:
                                                {
                                                    "captions": CAPTIONS(as list),
                                                    "medias": MEDIAS(as list)
                                                }
        """
        contents = json.load(
            open(self.multiple_posts_json_file_path, "r", encoding="utf-8"))
        return contents
