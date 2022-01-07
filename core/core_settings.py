PROJECT_FILEPATH = "/home/brandon/Documents/python-projects/simple-home-theater"
MEDIA_PLAYER = "mpv"
DEPLOYMENT_TYPE = "CLI"
# DEPLOYMENT_TYPE = "WEB"
APP_NAME = "Simple Home Theater"
AUTOPLAY_COUNTDOWN = 3#30
CONTENT_FILETYPES = ["mp4","mp3","opus"]

METADATA_LIST = ["plot","rating","runtimes"] #get these from imdbpy, there is a list in movie_scraper/main.py

USER_TABLE =  PROJECT_FILEPATH + "/data/users.csv"
CATEGORY_TABLE = PROJECT_FILEPATH + "/data/categories.csv"
CONTENT_TABLE = PROJECT_FILEPATH + "/data/contents.csv"
WATCH_TABLE = PROJECT_FILEPATH + "/data/watches.csv"


METADATA_LIST = ["name ","plot",'director','cast',"genre","runtimes"]
