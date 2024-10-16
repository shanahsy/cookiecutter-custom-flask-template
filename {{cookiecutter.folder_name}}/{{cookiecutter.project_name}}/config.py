"""{{cookiecutter.project_name}} development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (
    b'\xa5\xb9\x99F\n\xe1\x14\xf7\xdc\xcf[\xf5^a=W\x881\xa7\xa7\x8d$\x82\x1e'
)
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
{{cookiecutter.project_name}}_ROOT = pathlib.Path(__file__).resolve().parent.parent # type: ignore
UPLOAD_FOLDER = {{cookiecutter.project_name}}_ROOT/'var'/'uploads' # type: ignore
# UPLOAD_FOLDER = pathlib.Path('/var/www/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/{{cookiecutter.project_name}}.sqlite3
DATABASE_FILENAME = {{cookiecutter.project_name}}_ROOT/'var'/'{{cookiecutter.project_name}}.sqlite3' # type: ignore
