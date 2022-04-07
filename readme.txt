########################################
###NOT YOUR NORMAL NETFLIX AND CHILL!###
########################################

*The app is still in early stages*

-Features
==========
 - Customizable settings, change play next countdown, app name, goodbye message, app location, secure DB or Open acess and much more! 
 
 - Use your favorite media player! (CLI only)

 - CLI app and Web application. watch videos and play music from command line, local host or host a server 
 
 - Powerful CLI app! 
   * play content, string together content in order to play EX: 1 -p 
   * create playlists, play a playlist or string together playlists to play
   * playing content can be modified with extra arguments like 
     - shuffle
     - loop
     - auto play (play given content, then play rest of category)
     - change countdown 
     - grabbing content from another category (cross-content)

 -  Movie IMDB Data, Ask for a movie details and it will scrape IMDB for arguments supplied from settings, such as "Director", "actors", "Runtime", "genre", Etc
 
 - Open and Customizable databases, easy csv files.
     
     

HOW TO RUN:

###LINUX###
1- git clone https://github.com/yothebob/Simple-Home-Theater.git
2- activate venv (source simple-home-theater/bin/activate)
3- download dependencies "pip install -r requirements.txt"
4- run "python main.py"

###WINDOWS### (trying to build support for windows)
1- git clone https://github.com/yothebob/Simple-Home-Theater.git
2- change core/core-settings.py to use your data file locations  ex: USER_TABLE = "/data\users"
4- activate venv (source simple-home-theater\Scripts\activate.bat) ?
5- download dependencies "pip install -r requirements.txt"
6- run "python3 main.py"

