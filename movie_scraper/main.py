from imdb import IMDb
import os
import core.core_settings as settings

###SAMPLE SCRIPT###
# create an instance of the IMDb class

# ia = IMDb()
#
# noir_movie = ia.search_movie("D.O.A (1949)")
#
# print(noir_movie[0]["title"])
# print(noir_movie[0].movieID)
#
# doa = ia.get_movie(noir_movie[0].movieID)
#
# for genre in doa['genres']:
#     print(genre)


def get_content_id(filepath,obj_imdb):
    content_list = []
    for content in os.listdir(filepath):
        content_id = obj_imdb.search_movie(content)
        if len(content_id)  >= 1:
            content_list.append(content_id[0].movieID)
    return content_list


def get_content_variable(content_list,variable):
    variable_list = []
    for content in content_list
        get_content = obj_imdb.get_movie(content)
        title_list.append(get_content[variable])
    return title_list
