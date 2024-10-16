"""Views, one for each {{cookiecutter.project_name}} page."""
from {{cookiecutter.project_name}}.views.index import show_index
from {{cookiecutter.project_name}}.views.uploads import get_image
from {{cookiecutter.project_name}}.views.login import show_login, login, logout
from {{cookiecutter.project_name}}.views.accounts import show_create, show_delete
from {{cookiecutter.project_name}}.views.accounts import show_edit, show_password, account_auth
