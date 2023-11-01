"""Pages class"""
import os
import json
from instagrapi import Client
from instagrapi.types import Media, Story
from persiantools import jdatetime


class Page:
    """A class for prototyping pages.
    Args:
        scrapper (Client): scraper account thats gets datas from instagram server
        username (str): username of page
        project_directory_path (str): main directory of project (for recognizing
            "stories" and "posts" folder)
        jsons_files_name (str): name of jsons files of this page (for saving
            scrapped datas)
    """

    def __init__(
        self,
        scarpper: Client,
        username: str,
        directory_path_to_save_datas: str,
        jsons_files_name: str
    ):
        # Globalling page username
        self.username = username

        # Globalling scrapper account
        self.scrapper = scarpper

        # Globalling page infos :
        self.info = None  # User()
        self.id = str()
        self.full_name = str()
        self.stories_list = list()
        self.posts_list = list()

        # Initializing and globalling stories api(json file)
        self.stories_json_file_path = os.path.join(
            directory_path_to_save_datas, f"api/stories/{jsons_files_name}.json"
        )
        json.dump({}, open(self.stories_json_file_path, "w", encoding="utf-8"))

        # Initializing and globalling posts api(jsons file)
        self.single_posts_json_file_path = os.path.join(
            directory_path_to_save_datas, f"api/posts/{jsons_files_name}-single.json"
        )
        self.multiple_posts_json_file_path = os.path.join(
            directory_path_to_save_datas, f"api/posts/{jsons_files_name}-multiple.json"
        )
        json.dump({}, open(self.single_posts_json_file_path, "w", encoding="utf-8"))
        json.dump({}, open(self.multiple_posts_json_file_path, "w", encoding="utf-8"))

    def first_initialize(self):
        """Gets page basic infos, current posts and stories."""
        # info, id and fullname
        self.info = self.scrapper.user_info_by_username_v1(self.username)
        self.id = self.info.pk
        self.full_name = self.info.full_name

        # stories list
        self.stories_list = self.scrapper.user_stories_v1(self.id)

        # posts list
        self.posts_list = self.scrapper.user_medias_v1(self.id)

    def check_stories_update(self):
        """Checks whether new stories were uploaded or not.
        If yes, returns them as a list; otherwise returns an empty list.

        Returns:
            new_stories_list (list): List of new stories.(as Story)
        """
        # Getting stories from server
        updated_stories_list = self.scrapper.user_stories_v1(self.id)

        # Recognizing and adding new stories in new_stories_list
        new_stories_list = []
        old_stories_pk_list = []
        for story in self.stories_list:
            old_stories_pk_list.append(story.pk)
        for story in updated_stories_list:
            if story.pk not in old_stories_pk_list:
                new_stories_list.append(story)
        del old_stories_pk_list

        # Saving updated stories list in self.stories_list and deleting updated_stories_list
        self.stories_list = updated_stories_list[:]
        del updated_stories_list

        return new_stories_list

    def get_story_obj(self, story: Story):
        """Creates an story object and returns it as dict.

        Args:
            story (Story): Story obj of story

        Returns:
            story_obj (dict): with this algorithm -> {"story_pk": PK,
                                                     "story_type": TYPE,
                                                     "story_link": LINK
                                                    } 
        """
        # Determining story type
        story_type = ""  # "photo" or "video"
        if story.video_url is None:
            story_type = "photo"
        else:
            story_type = "video"

        # Creating story obj
        story_obj = {}
        if story_type == "photo":
            story_link = story.thumbnail_url
        elif story_type == "video":
            story_link = story.video_url

        story_obj.update(
            {
                "story_pk": story.pk,
                "story_type": story_type,
                "story_link": story_link
            }
        )

        return story_obj

    def check_posts_update(self):
        """Checks whether new posts were uploaded or not.
        If yes, returns them as a list; otherwise returns an empty list.

        Returns:
            new_posts_list (list): List of new posts.(as Media)
        """
        # Getting posts from server
        updated_posts_list = self.scrapper.user_medias_v1(self.id)

        # Recognizing and adding new posts in new_posts_list
        new_posts_list = []
        old_posts_pk_list = []
        for post in self.posts_list:
            old_posts_pk_list.append(post.pk)
        for post in updated_posts_list:
            if post.pk not in old_posts_pk_list:
                new_posts_list.append(post)
        del old_posts_pk_list

        # Saving updated posts list in self.posts_list and deleting updated_posts_list
        self.posts_list = updated_posts_list[:]
        del updated_posts_list

        return new_posts_list

    def get_post_slide_type(self, post: Media):
        """Determines the count of post slides.

        Args:
            post (Media): Media of post

        Returns:
            post_slide_type (str): "single" or "multiple"
        """
        # Determining post slide type
        post_slide_type = ""  # "single" or "multiple"
        if post.media_type in [1, 2]:
            post_slide_type = "single"
        elif post.media_type == 8:
            post_slide_type = "multiple"

        return post_slide_type

    def get_single_post_obj(self, post: Media):
        """Creates a single post object and returns post details as a dict.

        Args:
            post (Media): Media obj of post

        Returns:
            post_obj (dict): with this algorithm -> {"post_pk": PK,
                                                     "post_type": TYPE,
                                                     "post_caption": CAPTION,
                                                     "media_link": LINK
                                                    } 
        """
        # Initializing post type
        post_type = ""  # "photo" or "video" or "igtv" or "reel"
        if post.media_type == 1:
            post_type = "photo"
        elif ((post.media_type == 2) and (post.product_type == "feed")):
            post_type = "video"
        elif ((post.media_type == 2) and (post.product_type == "igtv")):
            post_type = "igtv"
        elif ((post.media_type == 2) and (post.product_type == "clips")):
            post_type = "reel"

        # Creating post obj
        post_obj = {}
        if post_type == "photo":
            media_link = str(post.image_versions2["candidates"][0]["url"])
        elif post_type == "video" or post_type == "igtv":
            media_link = str(post.video_url)
        elif post_type == "reel":
            media_link = str(post.video_url)

        post_obj.update(
            {
                "post_pk": post.pk,
                "post_type": post_type,
                "post_caption": post.caption_text,
                "media_link": media_link
            }
        )

        return post_obj

    def get_multiple_post_obj(self, media: Media):
        """Creates a  multiple post object and returns post details as a dict.

        Args:
            media (Media): Media obj of post

        Returns:
            post_obj (dict): with this algorithm -> {"post_pk": PK,
                                                     "post_caption": CAPTION,
                                                     "medias": {
                                                        NUMBER: {
                                                            "type": TYPE, "media_link": LINK
                                                            }
                                                        }
                                                    }

        """
        # Creating "medias" dictionary for using in post obj
        medias = {}  # dictionary of medias
        i = 1
        for local_media in media.resources:
            media_type = ""  # "photo" or "video"
            media_link = ""
            if local_media.media_type == 1:
                number = i
                media_type = "photo"
                media_link = local_media.thumbnail_url
            elif local_media.media_type == 2:
                number = i
                media_type = "video"
                media_link = local_media.video_url
            medias.update(
                {number: {"type": media_type, "media_link": media_link}}
            )
            i += 1

        # Creating post obj
        post_obj = {}  # a dict
        post_obj.update(
            {
                "post_pk": media.pk,
                "post_caption": media.caption_text,
                "medias": medias
            }
        )
        del i, medias

        return post_obj


def log_and_print(message: str, logsfile: open, be_printed=True):
    """Saves logs in a txt file and prints them if needed.

    Args:
        message (str): log message
        logsfile (open): txtlogs file with open() function
        be_printed (bool, optional): needed to be printed. Defaults to True.
    """
    # Writing logs in logsfile
    logsfile.writelines(message + "\n")
    # Printing logs if required
    if be_printed is True:
        print(message)


def check_stories(page: Page, logsfile: open):
    """Powered by Page.check_stories_update()
    Checks the page and prints logs in terminal and logsfile.
    If new stories were uploaded, returns them as a list, otherwise
    returns None.

    Args:
        page (Page): page that should be checked its stories
        logsfile (open): txt logsfile with open() function

    Returns:
        new_stories (list) or None: result
    """
    # Showing page username
    log_and_print(f"|\n|----{page.username}", logsfile)

    # Calling Page.check_stories_update() and save results in new_stories
    new_stories = page.check_stories_update()

    # Deciding for new_stories and return function result
    if len(new_stories) == 0:
        log_and_print("|    |---- × No storie(s).\n|", logsfile)
        json.dump({}, open(page.stories_json_file_path, "w", encoding="utf-8"))
        return None
    elif len(new_stories) > 0:
        log_and_print(
            f"|    |---- √ New {len(new_stories)} storie(s). downloading...", logsfile)
        return new_stories


def save_stories(page: Page, new_stories: list, logsfile: open):
    """Saves stories details in Page.stories_json_file_path with this algorithm:
        {
        "types": TYPES(as list),
        "links": LINKS(as list)
        }

    Args:
        page (Page): page that its new stories should be saved
        new_stories (list): new stories that got from check_stories() function
        logsfile (open): txtlogs file with open() function
    """
    # Creating "contents" dict and saving in Page.stories_json_file_path
    types = []
    links = []
    for story in new_stories:
        story_obj = page.get_story_obj(story)
        types.append(story_obj["story_type"])
        links.append(story_obj["story_link"])
    contents = {
        "types": types,
        "links": links
    }
    json.dump(
        contents, open(page.stories_json_file_path, "w", encoding="utf-8")
    )
    log_and_print("|    |---- √ Downloading completed.\n|", logsfile)


def check_posts(page: Page, logsfile: open):
    """Powered by Page.check_posts_update()
    Checks the page and prints logs in terminal and logsfile.
    If new posts were uploaded, returns them as a list with this algorithm:
    [new_single_posts(as list), new_multiple_posts(as list)], otherwise returns None.

    Args:
        page (Page): page that should be checked its posts
        logsfile (open): txt logsfile with open() function

    Returns:
        new_posts (list) or None: result
    """
    # Showing page username
    log_and_print(f"|\n|----{page.username}", logsfile)

    # Calling Page.check_posts_update() and save results in new_posts
    new_posts = page.check_posts_update()

    # Deciding for new_posts and return function result
    if len(new_posts) == 0:
        log_and_print("|    |---- × No post(s).\n|", logsfile)
        json.dump({}, open(page.single_posts_json_file_path,
                  "w", encoding="utf-8"))
        json.dump({}, open(page.multiple_posts_json_file_path,
                  "w", encoding="utf-8"))
        return None
    elif len(new_posts) > 0:
        log_and_print(
            f"|    |---- √ New {len(new_posts)} posts(s). downloading...", logsfile)
        new_single_posts = []
        new_multiple_posts = []
        for media in new_posts:
            post_slide_type = page.get_post_slide_type(media)
            if post_slide_type == "single":
                new_single_posts.append(media)
            elif post_slide_type == "multiple":
                new_multiple_posts.append(media)
        new_posts = [new_single_posts, new_multiple_posts]
        return new_posts


def save_single_posts(page: Page, new_single_posts: list, logsfile: open):
    """Saves single posts details in Page.single_posts_json_file_path with this algorithm:
        {
        "types": TYPES(as list),
        "captions": CAPTIONS(as list),
        "links": LINKS(as list)
        }

    Args:
        page (Page): page that its new posts should be saved
        new_single_posts (list): new single posts that got from check_posts()[0] function
        logsfile (open): txtlogs file with open() function
    """
    # Creating "contents" dict and saving in Page.single_posts_json_file_path
    types = []
    captions = []
    links = []
    for post in new_single_posts:
        post_obj = page.get_single_post_obj(post)
        types.append(post_obj["post_type"])
        captions.append(post_obj["post_caption"])
        links.append(post_obj["media_link"])
    contents = {
        "types": types,
        "captions": captions,
        "links": links
    }
    json.dump(
        contents, open(page.single_posts_json_file_path, "w", encoding="utf-8")
    )
    log_and_print("|    |---- √ Downloading completed.(single posts)\n|", logsfile)


def save_multiple_posts(page: Page, new_multiple_posts: list, logsfile: open):
    """Saves multiple posts details in Page.multiple_posts_json_file_path with this algorithm:
        {
        "captions": CAPTIONS(as list),
        "medias": MEDIAS(as list)
        }

    Args:
        page (Page): page that its new posts should be saved
        new_multiple_posts (list): new multiple posts that got from check_posts()[1] function
        logsfile (open): txtlogs file with open() function
    """
    # Creating "contents" dict and saving in Page.multiple_posts_json_file_path
    captions = []
    medias = []
    for post in new_multiple_posts:
        post_obj = page.get_multiple_post_obj(post)
        captions.append(post_obj["post_caption"])
        medias.append(post_obj["medias"])
    contents = {
        "captions": captions,
        "medias": medias
    }
    json.dump(
        contents, open(page.multiple_posts_json_file_path,
                       "w", encoding="utf-8")
    )
    log_and_print("|    |---- √ Downloading completed.(multiple posts)\n|", logsfile)


def scrap(logsfile: open, PROID: int, pages_list: list, has_result = False):
    # Logging and printing initial logs
    log_and_print("\n\n\n", logsfile)
    log_and_print(f"PROID: {PROID}", logsfile)
    log_and_print(f"STARTED: {jdatetime.JalaliDateTime.now()}", logsfile)
    log_and_print("===================================", logsfile)

    # Checking stories, logging and printing
    log_and_print("STORY CHECKING...", logsfile)
    for page in pages_list:
        new_stories = check_stories(page, logsfile)
        if new_stories is not None:
            save_stories(page, new_stories, logsfile)
            has_result = True

    log_and_print("===================================", logsfile)

    # Checking posts, logging and printing
    log_and_print("POST CHECKING...", logsfile)
    for page in pages_list:
        new_posts = check_posts(page, logsfile)
        if new_posts is not None:
            if new_posts[0] != []:
                save_single_posts(page, new_posts[0], logsfile)
            if new_posts[1] != []:
                save_multiple_posts(page, new_posts[1], logsfile)
            has_result = True

    # Logging and printing final logs
    log_and_print("===================================", logsfile)
    log_and_print(f"Ended: {jdatetime.JalaliDateTime.now()}", logsfile)

    return has_result
