"""
{{cookiecutter.project_name}} index (main) view.

URLs include:
/
"""
import flask
import {{cookiecutter.project_name}}


@{{cookiecutter.project_name}}.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session["username"]
    context = {"logname": logname}
    context["logged_in"] = True
    return flask.render_template("index.html", **context)

