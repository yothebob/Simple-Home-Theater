from imdb import IMDb
import os
import core.core_settings as settings
from core.orm import *
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

# https://github.com/alberanid/imdbpy/blob/master/imdb/Movie.py
 # keys_alias = {
 #        'tv schedule': 'airing',
 #        'user rating': 'rating',
 #        'plot summary': 'plot',
 #        'plot summaries': 'plot',
 #        'directed by': 'director',
 #        'directors': 'director',
 #        'writers': 'writer',
 #        'actors': 'cast',
 #        'actresses': 'cast',
 #        'aka': 'akas',
 #        'also known as': 'akas',
 #        'country': 'countries',
 #        'production country': 'countries',
 #        'production countries': 'countries',
 #        'genre': 'genres',
 #        'runtime': 'runtimes',
 #        'lang': 'languages',
 #        'color': 'color info',
 #        'cover': 'cover url',
 #        'full-size cover': 'full-size cover url',
 #        'seasons': 'number of seasons',
 #        'language': 'languages',
 #        'certificate': 'certificates',
 #        'certifications': 'certificates',
 #        'certification': 'certificates',
 #        'episodes number': 'number of episodes',
 #        'faq': 'faqs',
 #        'technical': 'tech',
 #        'frequently asked questions': 'faqs'
 #    }
 #


def clean_filename(file):
    '''a function for removing the file extension'''
    for index in range(len(file)-1,-1,-1):
        if file[index] == ".":
            return file[:index]
    return file


def get_content_id(content,obj_imdb):
    #one content
    imdb_content_list = []
    content_id = obj_imdb.search_movie(content)
    if len(content_id)  >= 1:
        imdb_content_list.append(content_id[0].movieID)
    else:
        imdb_content_list.append(f"could not find {content}")
    return imdb_content_list



def get_contents_id(content_list,obj_imdb):
    #multiple contents
    imdb_content_list = []
    for content in content_list:
        content_id = obj_imdb.search_movie(content)
        if len(content_id)  >= 1:
            imdb_content_list.append(content_id[0].movieID)
        else:
            imdb_content_list.append(f"could not find {content}")
    return imdb_content_list



def get_content_id_from_folder(filepath,obj_imdb):
    '''only works with reading from folder!'''
    content_list = []
    for content in os.listdir(filepath):
        content_id = obj_imdb.search_movie(content)
        if len(content_id)  >= 1:
            content_list.append(content_id[0].movieID)
        else:
            content_list.append(f"could not find {content}")
    return content_list



def get_content_variable(content,variable,obj_imdb):
    title_list = []
    try:
        get_content = obj_imdb.get_movie(content)
        title_list.append(get_content[variable])
    except:
        title_list.append(f"could not find {variable}")
    return title_list



def get_contents_variable(content_list,variable,obj_imdb):
    title_list = []
    for content in content_list:
        try:
            get_content = obj_imdb.get_movie(content)
            title_list.append(get_content[variable])
        except:
            title_list.append(f"could not find {variable}")
    return title_list

def find_metadata(filename,metadata_list=settings.METADATA_LIST):
    '''a function for using IMDB for content metadata, save to metadata DB'''
    Imdb = IMDb()
    print(f"finding metadata for {filename}...")

    content_data = query(settings.CONTENT_TABLE,filename,"name")
    cleaned_name = clean_filename(filename)
    res_list = []
    # res_list.append(content_data[0])#pk

    content_id = get_content_id(cleaned_name,Imdb)
    if content_id is not None:
        pass
        # res_list.append(content_id[0]) save content id
    else:
        pass
        # res_list.append("") or nothing

    for data in metadata_list:
        try:
            res_list.append(get_content_variable(content_id[0],data,Imdb))
        except:
            res_list.append("")

    # print(f"finished with {filename}")
    return res_list
    # use later
    # write_query(settings.METADATA_TABLE,res_list)
