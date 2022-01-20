import core.core_settings as settings

# run this file to run the program of your choice
if settings.DEPLOYMENT_TYPE == "CLI":
    import cli.main
elif settings.DEPLOYMENT_TYPE == "WEB":
    from webapp.main import *



# #testing movie scraper
# from movie_scraper.main import *
# from imdb import IMDb
# import os
#
#
# Imdb = IMDb()
# pi_path = "/run/user/1000/kio-fuse-BpWmnZ/smb/pi@raspberrypi.local/public/Movies"
#
# final_data = {}
# metadata_list = ["name ","plot",'director','cast'] #genre works
#
# #clean up filenames
# for file in os.listdir(pi_path):
#     cleaned_file = clean_filename(file)
#     final_data[cleaned_file] = []
#
# #
# for name in final_data.keys():
#     content_list = get_content_id(name,Imdb)
#     final_data[name] += content_list
#
# for data in metadata_list:
#     for name in final_data.keys():
#         try:
#             final_data[name] += get_content_variable(name,data,Imdb)
#         except:
#             print(f"{data} did not work")
#             continue;
# print("final",final_data)
