import os
PROJECT_FILEPATH = os.getcwd()
MEDIA_PLAYER = "mpv"
# DEPLOYMENT_TYPE = "CLI"
DEPLOYMENT_TYPE = "WEB"
APP_NAME = "Simple Home Theater"
GOODBYE = " hope to see you again soon! :)"
AUTOPLAY_COUNTDOWN = 3#30
CONTENT_FILETYPES = ["mp4","mp3","opus"]

METADATA_LIST = ["plot","rating","runtimes"] #get these from imdbpy, there is a list in movie_scraper/main.py
STATIC_DIR = "static"

STOREFRONT_USER = False
STOREFRONT_USER_NAME = "store"
STOREFRONT_USER_PASS = "store"

USER_TABLE =  PROJECT_FILEPATH + "/data/users.csv"
CATEGORY_TABLE = PROJECT_FILEPATH + "/data/categories.csv"
CONTENT_TABLE = PROJECT_FILEPATH + "/data/contents.csv"
WATCH_TABLE = PROJECT_FILEPATH + "/data/watches.csv"
PLAYLIST_TABLE = PROJECT_FILEPATH + "/data/playlists.csv"
PLAYLIST_CONTENT_TABLE = PROJECT_FILEPATH + "/data/playlist_contents.csv"
CONTENT_METADATA_TABLE = PROJECT_FILEPATH + "/data/content_metadatas.csv"
