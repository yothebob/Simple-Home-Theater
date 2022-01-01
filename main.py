import core.core_settings as settings

# run this file to run the program of your choice
if settings.DEPLOYMENT_TYPE == "CLI":
    import cli.main
elif settings.DEPLOYMENT_TYPE == "WEB":
    import webapp.main



# #testing movie scraper
# from movie_scraper.main import *
# from imdb import IMDb
# import os
#
#
# find_metadata('The Killing (1956).ogx')
