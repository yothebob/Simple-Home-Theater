import core.core_settings as settings
import fileinput

#run this file to run the program of your choice
# if settings.DEPLOYMENT_TYPE == "CLI":
#     import cli.main
# elif settings.DEPLOYMENT_TYPE == "WEB":
#     import webapp.main

# writes on top of the line
# f = open("/home/brandon/Documents/python-projects/simple-home-theater/data/categories.csv", "r")
# contents = f.readlines()
# f.close()
#
# contents.insert(index, "1,1,Music,brandon,/home/brandons/Music, testing")
#
# f = open("/home/brandon/Documents/python-projects/simple-home-theater/data/categories.csv", "w")
# contents = "".join(contents)
# f.write(contents)
# f.close()

for line in fileinput.FileInput("/home/brandon/Documents/python-projects/simple-home-theater/data/categories.csv",inplace=1):
    if "2" in line:
        line = line.replace(line,"1,1,Music,brandon,/home/brandons/Music, testing")
