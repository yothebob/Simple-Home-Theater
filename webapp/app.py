from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from flask import Flask, render_template, request, g, url_for, send_file
from webapp.forms import LoginForm, CreateUserForm, AddCategoryForm
from movie_scraper.main import find_metadata

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
    return render_template("create_user.html",create_form=create_form)



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
def show_content_page(category_name,content_name):
    for cont in FlaskApp.user.current_category.content_list:
        if cont.name == content_name:
            content = cont
            content_path = f'{content.category.folder_location}/"{content.name}"'
            content_metadata = find_metadata(content.name)
            return render_template("content_page.html",instance=FlaskApp.user,content=content,
            content_metadata=content_metadata,content_path=content_path)

    error = "no content found! please try again"
    return render_template("content_page.html",instance=FlaskApp.user)

app.run()
