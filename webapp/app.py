from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from flask import Flask, render_template, request, g, url_for

class FlaskApp(App):

    app = Flask(__name__)
    app.config['SECRET KEY'] = '1233456789'

    app.static_folder = "static"

    def create_user(self,username,password,password_again):
        '''create and save a new user to database '''
        username_taken = query(settings.PROJECT_FILEPATH +"/data/users.csv",username)
        if username_taken is not None:
            if username_taken[1] == username:
                return render_template("login.html")# username taken
        if password != password_again:
            return render_template("login.html")# passwords dont match
        write_query(settings.PROJECT_FILEPATH + "/data/users.csv",[username,password,[],[]])
        return render_template("login.html") # user created. go to login

    def login(self,username,password):
        verify_credidentials = query(settings.PROJECT_FILEPATH + "/data/users.csv", username)
        if verify_credidentials is not None:
            #user found, attempting to authenticate
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                instance = self.load_user(verify_credidentials[0])
                '''take to movie screen'''
                return render_template("home.html",instance=instance)
            else:
                #not right credidentials
                return render_template("login.html")
        else:
            #query could not find user
            return render_template("login.html")


    def delete_user(self,username,password,password_again):
        if password == password_again:
            verify_credidentials = query(settings.PROJECT_FILEPATH + "/data/users.csv", username)
        if verify_credidentials:
            if verify_credidentials[1] == username and verify_credidentials[2] == password:
                delete_query(settings.PROJECT_FILEPATH + "/data/users.csv",username)
                return render_template("base.html")
        return render_template("base.html")
