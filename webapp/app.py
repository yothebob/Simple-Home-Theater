from core.app import App
from core.models import Category, User, Genre, Tag, Content
from core.orm import query, write_query, delete_query
import core.core_settings as settings
from flask import Flask, render_template, request, g, url_for, send_from_directory, redirect
from webapp.forms import LoginForm, CreateUserForm, AddCategoryForm, SearchCategoryForm
from movie_scraper.main import find_metadata
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

FlaskApp = App()


app = Flask(__name__)


app.static_folder = settings.STATIC_DIR
app.secret_key = "qp2e4fjaefvp0oLSD#_*$gfASD*^24WEF8f"


login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = FlaskApp.load_userz(user_id)
    return user

@app.route("/")
def home_page():
    app_name = settings.APP_NAME
    return render_template("index.html",app_name=app_name)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    print(current_user)
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm(request.form)
    if request.method == "POST":
        instance = FlaskApp.login(login_form.username.data,login_form.password.data)
        if isinstance(instance,User):
            login_user(instance)
            return render_template("home.html",instance=current_user)
        else:
            #error
            return render_template("login.html",error=instance[1],login_form=login_form)
    else:
        return render_template("login.html",login_form=login_form)



@app.route("/create/",methods=["GET","POST"])
@login_required
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



# @login_required
@app.route("/home/",methods=["GET","POST"])
def application():
    # create playlists here and stuff
    display_amount = 10
    return render_template("home.html",instance=current_user)


# @login_required
@app.route("/category/",methods=["GET","POST"])
def show_categories():
    user_categories = current_user.categories
    return render_template("show_categories.html",instance=current_user, user_categories=user_categories)


@app.route("/category/add/",methods=["GET","POST"])
@login_required
def add_category():
    add_category_form = AddCategoryForm(request.form)

    if request.method == "POST":
        print("adding category")
        current_user.add_category(add_category_form.name.data,add_category_form.filepath.data)
    return render_template("add_category.html",add_category_form=add_category_form)

def im_feeling_lucky():
    # this will return a random recommendation, maybe most watched or etc
    pass

@app.route("/category/<category_name>",methods=["GET","POST"])
@login_required
def show_category(category_name):
    search_category_form = SearchCategoryForm(request.form)
    for cat in current_user.categories:
        if cat.name == category_name:
            current_user.current_category = cat
            category = current_user.current_category
            break
    if request.method == "POST":
        search_string = search_category_form.search.data
        if search_string != "":
            search_results = [current_user.current_category.content_list[index] for index in range(len(current_user.current_category.content_list)) if search_string.lower() in current_user.current_category.content_list[index].name.lower()]
            return render_template("show_category.html",instance=current_user,category=category, search_results=search_results,search_string=search_string, search_category_form=search_category_form )
    return render_template("show_category.html",instance=current_user,category=category,search_category_form=search_category_form)


@app.route("/category/<category_name>/<content_name>",methods=["GET","POST"])
@login_required
def show_content_page(category_name,content_name):
    for cont in current_user.current_category.content_list:
        if cont.name == content_name:
            content = cont
            content_path = f"{content.category.folder_location}"
            if ".html" in content_name:
                content_file = open(f"{content_path}/{content_name}", "r")
                content_text_raw = content_file.readlines()
                content_text = "".join(content_text_raw).replace("\n","")
                content_file.close()
                return render_template("nonmedia_content_page.html",instance=current_user,content=content,
                                    content_text=content_text,content_path=content_path,error="")

            else:
                content_metadata = find_metadata(content.name)
                return render_template("content_page.html",instance=current_user,content=content,
                                   content_metadata=content_metadata,content_path=content_path,error="")

    error = "no content found! please try again"
    return render_template("content_page.html",instance=current_user,error=error)


@app.route("/play/")
@login_required
def send_content():
    file_id = request.args.get("file",None)
    for cont in current_user.current_category.content_list:
        if cont.pk == file_id:
            content = cont
            current_user.append_watched(content)
            return send_from_directory(current_user.current_category.folder_location,content.name,as_attachment=False)
    return "sorry, could not find the video :(("


app.run()
