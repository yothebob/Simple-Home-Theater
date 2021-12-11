import core.core_settings as settings

#run this file to run the program of your choice
# if settings.DEPLOYMENT_TYPE == "CLI":
#     import cli.main
# elif settings.DEPLOYMENT_TYPE == "WEB":
#     import webapp.main



#write_query one line

db_rows = [row for row in open("/home/brandon/Documents/python-projects/simple-home-theater/data/categories.csv", "r")]
print(db_rows)

f = open("/home/brandon/Documents/python-projects/simple-home-theater/data/categories.csv", "w")
for row in db_rows:
    if "2" in row:
        new_line = "1,1,Music,brandon,/home/brandons/Music, testing\n"
        f.write(new_line)
    else:
        f.write(row)
f.close()
