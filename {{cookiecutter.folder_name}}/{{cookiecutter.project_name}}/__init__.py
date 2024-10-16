"""{{cookiecutter.project_name}} package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Read settings from config module ({{cookiecutter.project_name}}/config.py)
app.config.from_object('{{cookiecutter.project_name}}.config')

# Overlay settings read from a Python file whose path is set in the environment
# variable {{cookiecutter.project_name}}_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export {{cookiecutter.project_name}}_SETTINGS=secret_key_config.py
app.config.from_envvar('{{cookiecutter.project_name}}_SETTINGS', silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import {{cookiecutter.project_name}}.views  # type: ignore # noqa: E402  pylint: disable=wrong-import-position
import {{cookiecutter.project_name}}.model  # type: ignore # noqa: E402  pylint: disable=wrong-import-position
