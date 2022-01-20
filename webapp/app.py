from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from flask import Flask, render_template, request, g, url_for
from webapp.forms import LoginForm, CreateUserForm, AddCategoryForm

FlaskApp = App()


app = Flask(__name__)

@app.route("/")
def home_page():
    app_name = settings.APP_NAME
    return render_template("index.html",app_name=app_name)


@app.route("/login/",methods=["GET","POST"])
def login_page():

    login_form = LoginForm(request.form)
    print(login_form)
    if request.method == "POST":
        instance = FlaskApp.login(login_form.username.data,login_form.password.data)
        if isinstance(instance,User):
            FlaskApp.user = instance
            #successful login
            return render_template("home.html",instance=instance)
        else:
            #error
            return render_template("login.html",error=instance[1],login_form=login_form)
    else:
        return render_template("login.html",login_form=login_form)


@app.route("/create/",methods=["GET","POST"])
def create_user_page():
    '''create and save a new user to database '''
    create_form = CreateUserForm(request.form)
    login_form = LoginForm(request.form)
    if request.method == "POST":
        print("posted")
        new_user = FlaskApp.create_user(create_form.username.data,create_form.password.data,create_form.password_again.data)
        if isinstance(new_user,str):
            print(f"error: {new_user}")
            return render_template("create_user.html",error=new_user[1],create_form=create_form)
        else:
            print("success! routing to login")
            return render_template("login.html",login_form=login_form)


@app.route("/home/",methods=["GET","POST"])
def application():
    # create playlists here and stuff
    display_amount = 10
    return render_template("home.html",instance=FlaskApp.user)


@app.route("/category/",methods=["GET","POST"])
def show_categories():
    user_categories = FlaskApp.user.categories
    return render_template("show_categories.html",instance=FlaskApp.user, user_categories=user_categories)


@app.route("/category/add/",methods=["GET","POST"])
def add_category():
    add_category_form = AddCategoryForm(request.form)

    if request.method == "POST":
        print("adding category")
        self.user.add_category()
    return render_template("add_category.html",add_category_form=add_category_form)


@app.route("/category/<category_name>",methods=["GET","POST"])
def show_category(category_name):
    for cat in FlaskApp.user.categories:
        if cat.name == category_name:
            FlaskApp.user.current_category = cat
            category = FlaskApp.user.current_category
            break
    return render_template("show_category.html",instance=FlaskApp.user,category=category)


@app.route("/category/<category_name>/<content_name>",methods=["GET","POST"])
def content_page(content_name):
    for cont in FlaskApp.user.current_category:
        if cont.name == content_name:
            content = cont
            break
    return render_template("content_page.html",instance=FlaskApp.user,content=content)


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
