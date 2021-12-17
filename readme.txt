
HOW TO RUN:

###LINUX###
1- git clone https://github.com/yothebob/Simple-Home-Theater.git
2- change core/core-settings.py to use your file location  ex: PROJECT_FILEPATH = "/path/to/simple-home-theater"
3- activate venv (source simple-home-theater/bin/activate)
4- download dependencies "pip install -r requirements.txt"
5- run "python main.py"

###WINDOWS### (trying to build support for windows)
1- git clone https://github.com/yothebob/Simple-Home-Theater.git
2- change core/core-settings.py to use your file location  ex: PROJECT_FILEPATH = "\path\to\simple-home-theater"
3- change core/core-settings.py to use your data file locations  ex: USER_TABLE = "/data\users"
4- activate venv (source simple-home-theater\Scripts\activate.bat) ?
5- download dependencies "pip install -r requirements.txt"
6- run "python3 main.py"


CLI VS WEB
 If you want to switch app type just chane it in your core/core_settings.py

 DEPLOYMENT_TYPE = "CLI"
 # DEPLOYMENT_TYPE = "WEB"


HOW IT WORKS:

  object Models:
    - user
      login in with a username/password to have instances of categories, content, metadata and content lists based off watched/ favorites

    - category
      created and accessable to the user that created it, stores media content (a file/ file location)

    -content
      A peice of media content to play, stored in a category. will store metadata from a movie scraper

    \/in progress \/
    - Genre
    -content list
    -tag


The base app is in core. and the deployable apps are inheriting from core. core.models stores all the models/ model functions. all model things should be put in core.models! core.core_settings will have all the adjustable settings for your deployable app (in the main.py). each app.py has the core functions of login, create and etc. pre application tools. cli.main.py/web.main.py will be the app after login functions.

ORM
for now the master uses csv as DB files and my own custom ORM (is under core.orm.py). I will make a branch for using sql, branch off master-sql if you want to use sql.



so far..
