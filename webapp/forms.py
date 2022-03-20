from wtforms import Form, SelectField, SubmitField, validators, RadioField,StringField
from wtforms.widgets import PasswordInput

class LoginForm(Form):

    username = StringField("Username:")
    password = StringField("Password:", widget=PasswordInput(hide_value=False))
    submit = SubmitField("Log In")

class CreateUserForm(Form):

    username = StringField("Username:")
    password = StringField("Password:", widget=PasswordInput(hide_value=False))
    password_again = StringField("Password again:", widget=PasswordInput(hide_value=False))
    submit = SubmitField("Create User")

class AddCategoryForm(Form):
    name = StringField("Category Name:")
    filepath = StringField("filepath:")
    submit = SubmitField("Add Category")

class SearchCategoryForm(Form):
    search = StringField("")
    submit = SubmitField("Search")
