from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from flask import Flask, render_template, request, g, url_for
from webapp.forms import LoginForm, CreateUserForm

#class FlaskApp():
# def __init__(app):
    # app = app
    # self.app.config['SECRET KEY'] = '1233456789'
    # instance = ""
    # self.app.static_folder = "static"
#



app = Flask(__name__)

@app.route("/")
def home_page():
    app_name = settings.APP_NAME
    return render_template("home.html",app_name=app_name)

sht_app = App()


@app.route("/login/",methods=["GET","POST"])
def login():

    login_form = LoginForm(request.form)
    print(login_form)
    error = ""
    if request.method == "POST":
        verify_credidentials = query(settings.USER_TABLE, login_form.username.data)
        print("posted")
        print("credidentials: ",verify_credidentials)
        if verify_credidentials is not None:
            #user found, attempting to authenticate
            if verify_credidentials[1] == login_form.username.data and verify_credidentials[2] == login_form.password.data:
                instance = sht_app.load_user(verify_credidentials[0]) #loading with pk
                '''take to movie screen'''
                return render_template("home.html",instance=instance)
            else:
                #not right credidentials
                error = "Username of Password is not correct."
                return render_template("login.html",error=error,login_form=login_form)
        else:
            #query could not find user
            error = "Could not find user"
            return render_template("login.html",error=error,login_form=login_form)
    else:
        return render_template("login.html",login_form=login_form)


@app.route("/create/",methods=["GET","POST"])
def create_user():
    '''create and save a new user to database '''
    create_form = CreateUserForm(request.form)
    if request.method == "POST":
        username_taken = query(settings.USER_TABLE,create_form.username.data)
        if username_taken is not None:
            if username_taken[1] == create_form.username.data:
                error = "Username Taken."
                return render_template("login.html",error=error)# username taken

        if create_form.password.data != create_form.password_again.data:
            error = "Passwords don't match, please try again."
            return render_template("login.html",error=error)# passwords dont match

        write_query(settings.USER_TABLE,[create_form.username.data,create_form.password.data,[],[]])
        return render_template("login.html") # user created. go to login
    else:
        return render_template("login.html")



# flaskapp = FlaskApp(site)
# if __name__ == "__main__":
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
