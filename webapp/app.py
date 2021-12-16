from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from flask import Flask, render_template, request, g, url_for
from webapp.forms import LoginForm, CreateUserForm

class FlaskApp(App):
    app = Flask(__name__)
    app.config['SECRET KEY'] = '1233456789'
    instance = ""
    # app.static_folder = "static"


    app.route("/")
    def home_page(self):
        app_name = settings.APP_NAME
        render_template("home.html",app_name=app_name)


    app.route("/login/",methods=["GET","POST"])
    def login(self):

        login_form = LoginForm(request.form)
        error = ""
        if request.method == "POST":
            verify_credidentials = query(settings.PROJECT_FILEPATH + settings.USER_TABLE, login_form.username.data)
            if verify_credidentials is not None:
                #user found, attempting to authenticate
                if verify_credidentials[1] == login_form.username.data and verify_credidentials[2] == login_form.password.data:
                    self.instance = self.load_user(verify_credidentials[0]) #loading with pk
                    '''take to movie screen'''
                    return render_template("home.html",instance=self.instance)
                else:
                    #not right credidentials
                    error = "Username of Password is not correct."
                    return render_template("login.html",error=error)
            else:
                #query could not find user
                error = "Could not find user"
                return render_template("login.html",error=error)


    app.route("/create/",methods=["GET","POST"])
    def create_user(self):
        '''create and save a new user to database '''
        create_form = CreateUserForm(request.form)
        if request.method == "POST":
            username_taken = query(settings.PROJECT_FILEPATH +settings.USER_TABLE,create_form.username.data)
            if username_taken is not None:
                if username_taken[1] == create_form.username.data:
                    error = "Username Taken."
                    return render_template("login.html",error=error)# username taken

            if create_form.password.data != create_form.password_again.data:
                error = "Passwords don't match, please try again."
                return render_template("login.html",error=error)# passwords dont match

            write_query(settings.PROJECT_FILEPATH + settings.USER_TABLE,[create_form.username.data,create_form.password.data,[],[]])
            return render_template("login.html") # user created. go to login

    app.run()

    # run_webapp()
    #currently not working (havent even tried)
    # app.route("/delete/",methods=["GET","POST"])
    # def delete_user(self,username,password,password_again):
    #     if password == password_again:
    #         verify_credidentials = query(settings.PROJECT_FILEPATH + "/data/users.csv", username)
    #     if verify_credidentials:
    #         if verify_credidentials[1] == username and verify_credidentials[2] == password:
    #             delete_query(settings.PROJECT_FILEPATH + "/data/users.csv",username)
    #             return render_template("base.html")
    #     return render_template("base.html")
