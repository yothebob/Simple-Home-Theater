from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from flask import Flask, render_template, request, g, url_for
from webapp.forms import LoginForm, CreateUserForm, AddCategoryForm

#class FlaskApp():
# def __init__(app):
    # app = app
    # self.app.config['SECRET KEY'] = '1233456789'
    # instance = ""
    # self.app.static_folder = "static"
#




class FlaskApp():
    app = Flask(__name__)

    def __init__(self):
        self.user = ""
        self.sht_app = App()
        sht_app = self.sht_app
        user = self.user

    @app.route("/")
    def home_page():
        app_name = settings.APP_NAME
        return render_template("index.html",app_name=app_name)


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
                    user = sht_app.load_user(verify_credidentials[0]) #loading with pk
                    print(user.username)
                    '''take to movie screen'''
                    return render_template("home.html",instance=user)
                else:
                    #not right credidentials
                    error = "Username of Password<h3>{{category}}</h3> is not correct."
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
        login_form = LoginForm(request.form)
        if request.method == "POST":
            print("posted")
            username_taken = query(settings.USER_TABLE,create_form.username.data)
            if username_taken is not None:
                if username_taken[1] == create_form.username.data:
                    error = "Username Taken."
                    print('Username Taken')
                    return render_template("create_user.html",error=error,create_form=create_form)# username taken

            if create_form.password.data != create_form.password_again.data:
                error = "Passwords don't match, please try again."
                print("passwords dont match")
                return render_template("create_user.html",error=error,create_form=create_form)# passwords dont match

            else:
                print("success! routing to login")
                write_query(settings.USER_TABLE,[create_form.username.data,create_form.password.data,[],[]])
                return login() # user created. go to login
        else:
            return render_template("create_user.html",create_form=create_form)



    @app.route("/home/",methods=["GET","POST"])
    def application():
        # create playlists here and stuff
        display_amount = 10
        return render_template("home.html",instance=self.user)


    @app.route("/category/",methods=["GET","POST"])
    def show_categories():
        user_categories = self.user.load_categories()
        return render_template("show_categories.html",user_categories=user_categories)


    @app.route("/category/add/",methods=["GET","POST"])
    def add_category():
        add_category_form = AddCategoryForm(request.form)

        if request.method == "POST":
            print("adding category")
            self.user.add_category()
        return render_template("add_category.html",add_category_form=add_category_form)


    @app.route("/category/<category>",methods=["GET","POST"])
    def show_category(category):
        return render_template()

    app.run()

# command_dictionary = {
#     "add"    : ["add","-a","-add","--add"],
#     "sync" : ["sync", "-s", "--sync", "reload", "load"],
#     "watched": ["watched", "--watched", "-watched" , "-w", "watch", "--watch"],
#     "passwd" : ["passwd", "--passwd", "password", "-p", "--password"],
#     "exit"   : ["exit", "end", "-e", "--end", "--exit"],
#     "help"   : ["help","-h","--help"],
#     "category" : ["cat", "category", "-cat", "--category","ls"]
# }
# if user_input.lower() in command_dictionary["help"]:
#     print("Commands: ")
#     print([print(key,val) for key, val in command_dictionary.items()])
#     return main_page(user)
#
# elif user_input.lower() in command_dictionary["category"]:
#     user_categories = user.load_categories()
#     show_user_categories(user_categories)
#     user_input = input(": ")
#     if user_input.isnumeric():
#         picked_category = user_categories[int(user_input)]
#         user.current_category = picked_category
#         print(f"in {user.current_category.name} category...")
#         get_command = input(": ")
#         # user.create_playlist()
#         run_command = content_commands(user,picked_category,get_command)
#     else:
#         print("not valid")
#         return main_page(user)
#     while get_command.lower() != "exit":
#         get_command = input(": ")
#         # user.create_playlist()
#         run_command = content_commands(user,picked_category,get_command)
#     return main_page(user)
#
# elif user_input.lower() in command_dictionary["add"]:
#      user.add_category()
#      return main_page(user)
#
# elif user_input.lower() in command_dictionary["sync"]:
#     user.sync_categories()
#     return main_page(user)
#
# elif user_input.lower() in command_dictionary["watched"]:
#     user.get_watched()
#     return main_page(user)
#
# elif user_input.lower() in command_dictionary["passwd"]:
#     user.change_password()
#     return main_page(user)
#
# elif user_input.lower() in command_dictionary["exit"]:
#     exit()
#
# else:
#     print("Sorry please try Again")
#     return main_page(user)
#
