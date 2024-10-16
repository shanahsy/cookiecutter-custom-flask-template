"""REST API for posts."""
import sys
import flask
import insta485
from {{cookiecutter.project_name}}.views.login import check_credentials

LOGGER = flask.logging.create_logger({{cookiecutter.project_name}}.app)

@{{cookiecutter.project_name}}.app.errorhandler(403)
def forbidden_error(error):
    """Catch abort in access control and add json."""
    print(error)
    response = flask.jsonify({
        "message": "Access forbidden",
        "status_code": 403
    })
    return response, 403


def access_control():
    """Will abort 403 if username not in db or incorrect password."""
    try:
        # Try to get the username from the Authorization header
        if flask.request.authorization:
            username = flask.request.authorization['username']
            password = flask.request.authorization['password']

            check_credentials(username, password)  # Will abort 403 if wrong
        else:
            # Fallback to session
            username = flask.session["username"]
    except KeyError:
        # If neither authorization nor session is provided, abort with 403
        # return flask.jsonify({
        # "message": "Access forbidden",
        # "status_code": 403
        # })
        return flask.abort(403), 403

    return username