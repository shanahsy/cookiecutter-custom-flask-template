"""{{cookiecutter.project_name}} login view."""
import uuid
import os
import pathlib
import hashlib
import flask
import {{cookiecutter.project_name}}

LOGGER = flask.logging.create_logger({{cookiecutter.project_name}}.app)


@{{cookiecutter.project_name}}.app.route('/accounts/login/')
def show_login():
    """Display /accounts/login/ route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    return flask.render_template('login.html')


def get_password_from_db(connection, username):
    """Get hashed password from db."""
    cur = connection.execute(
        "SELECT password from users "
        "WHERE username = ?",
        (username, )
    )

    return cur.fetchone()


def verify_password(password_list, password):
    """Create hashed password."""
    algorithm = password_list[0]
    salt = password_list[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))

    return hash_obj.hexdigest()


def hash_password_uuid(password):
    """Create hashed password using uuid."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()

    return "$".join([algorithm, salt, password_hash])


def delete_file(file_dict):
    """Delete file from file system if it exists."""
    filename = file_dict["filename"]
    path = {{cookiecutter.project_name}}.app.config["UPLOAD_FOLDER"]/filename

    LOGGER.debug("image filename = %s", filename)

    # Check if the file exists
    if os.path.exists(path):
        os.remove(path)  # Delete the file
        LOGGER.debug("File %s has been deleted.", {filename})
    else:
        LOGGER.debug("The file does not exist.")


def compute_basename(fileobj):
    """Compute and save uuid_basename to disk."""
    filename = fileobj.filename

    # Check file is not empty
    if fileobj.filename == '':
        LOGGER.debug("Trying to create a post with any empty file")
        flask.abort(400)

    # Compute base name (filename without directory).
    # We use a UUID to avoid clashes with existing files,
    # and ensure that the name is compatible with the
    # filesystem. For best practive, we ensure uniform
    # file extensions (e.g. lowercase).
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    path = {{cookiecutter.project_name}}.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    LOGGER.debug("fileobj = %s", uuid_basename)

    return uuid_basename


def do_delete():
    """Execute account delete."""
    # Connect to database
    connection = {{cookiecutter.project_name}}.model.get_db()
    if 'username' not in flask.session:
        flask.abort(403)

    username = flask.session['username']

    LOGGER.debug("Username: %s", username)
    LOGGER.debug("Username type: %s", type(username))

    # Get user profile filename from db so we can delete from filesystem
    cur = connection.execute(
        "SELECT filename from users "
        "WHERE username = ? ",
        (username, username, )
    )
    filenames = cur.fetchall()

    for file_dict in filenames:
        delete_file(file_dict)

    # Delete from users
    connection.execute(
        "DELETE FROM users "
        "WHERE username = ?",
        (username, )
    )

    flask.session.clear()


def check_credentials(username, password):
    """Check username and login against db."""
    # Connect to database
    connection = {{cookiecutter.project_name}}.model.get_db()

    # Get hashed password from db
    result = get_password_from_db(connection, username)

    # Check if user not in db
    if not result:
        LOGGER.debug("Username not in database")
        flask.abort(403)

    db_full_pass = result['password']
    password_list = db_full_pass.split("$")

    # Compute hashed password to be used in login and create
    password_hash = verify_password(password_list, password)

    if password_list[2] != password_hash:
        LOGGER.debug("Incorrect password")
        LOGGER.debug("Password hash: %s", password_hash)
        flask.abort(403)


def do_login():
    """Execute account login."""
    username = flask.request.form['username']
    password = flask.request.form['password']

    if not username:
        LOGGER.debug("Username is required")
        flask.abort(400)

    if not password:
        LOGGER.debug("Password is required")
        flask.abort(400)

    check_credentials(username, password)
    LOGGER.debug("Logged in sucessfully as %s", username)
    flask.session['username'] = username
    # Redirect to client is below


def do_create():
    """Execute account create."""
    # Connect to database
    connection = {{cookiecutter.project_name}}.model.get_db()
    username = flask.request.form['username']
    password = flask.request.form['password']

    if not username:
        LOGGER.debug("Username is required")
        flask.abort(400)

    if not password:
        LOGGER.debug("Password is required")
        flask.abort(400)

    fullname = flask.request.form['fullname']
    email = flask.request.form['email']

    if not fullname:
        LOGGER.debug("Username is fullname")
        flask.abort(400)

    if not email:
        LOGGER.debug("Password is email")
        flask.abort(400)

    # Unpack the flask object
    fileobj = flask.request.files["file"]
    uuid_basename = compute_basename(fileobj)
    password_db_string = hash_password_uuid(password)

    # Insert user into db
    connection.execute(
        "INSERT INTO users "
        "(username, fullname, email, filename, password) VALUES "
        "(?, ?, ?, ?, ?)",
        (username, fullname, email, uuid_basename, password_db_string)
    )

    LOGGER.debug("Logged in sucessfully as %s", username)
    flask.session['username'] = username


def do_edit_account():
    """Execute edit_account."""
    # Connect to database
    connection = {{cookiecutter.project_name}}.model.get_db()
    if 'username' not in flask.session:
        # Abort because user isn't logged in
        flask.abort(403)

    username = flask.session['username']

    fullname = flask.request.form['fullname']
    email = flask.request.form['email']

    if not fullname:
        flask.abort(400)

    if not email:
        flask.abort(400)

    # Unpack the flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    # Check if file is empty
    if fileobj.filename == '':
        # Update only username and email
        cur = connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ? "
            "WHERE username = ?",
            (fullname, email, username, )
        )

    else:
        # Delete old file
        cur = connection.execute(
            "SELECT filename from users "
            "WHERE username = ? ",
            (username, )
        )
        result = cur.fetchone()
        filename = result["filename"]
        path = {{cookiecutter.project_name}}.app.config["UPLOAD_FOLDER"]/filename

        LOGGER.debug("image filename = %s", filename)

        # Check if the file exists
        if os.path.exists(path):
            os.remove(path)  # Delete the file
            LOGGER.debug("File %s has been deleted.", {filename})
        else:
            LOGGER.debug("The file does not exist.")

        # Compute base name (filename without directory).
        # We use a UUID to avoid clashes with existing files,
        # and ensure that the name is compatible with the
        # filesystem. For best practive, we ensure uniform
        # file extensions (e.g. lowercase).
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save to disk
        path = {{cookiecutter.project_name}}.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        LOGGER.debug("fileobj = %s", uuid_basename)

        # Update in db
        cur = connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?, filename = ?"
            "WHERE username = ?",
            (fullname, email, uuid_basename, username, )
        )


def do_update_password():
    """Execute update_password."""
    # Connect to database
    connection = {{cookiecutter.project_name}}.model.get_db()
    if 'username' not in flask.session:
        # Abort because user isn't logged in
        flask.abort(403)

    username = flask.session['username']
    newpassword1 = flask.request.form['new_password1']
    newpassword2 = flask.request.form['new_password2']
    password = flask.request.form['password']

    if not newpassword1 or not newpassword2 or not password:
        flask.abort(400)

    # Get hashed password from db
    result = get_password_from_db(connection, username)

    # Check if user not in db
    if not result:
        LOGGER.debug("Password incorrect")
        flask.abort(403)

    db_full_pass = result['password']
    password_list = db_full_pass.split("$")

    # Compute hashed password to be used in login and create
    password_hash = verify_password(password_list, password)

    if password_list[2] != password_hash:
        flask.abort(403)

    if newpassword1 != newpassword2:
        LOGGER.debug("Passwords must match")
        flask.abort(401)

    password_db_string = hash_password_uuid(newpassword1)

    connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE username = ?",
        (password_db_string, username, )
    )


@{{cookiecutter.project_name}}.app.route('/accounts/', methods=['POST'])
def login():
    """Display /accounts/ routes."""
    operation = flask.request.form['operation']
    LOGGER.debug("Operation: %s", flask.request.form['operation'])

    if operation == 'delete':
        do_delete()
    elif operation == 'login':
        do_login()
    elif operation == 'create':
        do_create()
    elif operation == 'edit_account':
        do_edit_account()
    elif operation == 'update_password':
        do_update_password()

    # Redirect the client with flask.redirect()
    target = flask.request.args.get('target')
    if not target:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)


@{{cookiecutter.project_name}}.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Display /logout/ route."""
    # POST-only route for handling logout requests
    print("DEBUG Logout:", flask.session['username'])
    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))
