from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
    """homepage that redirects to register."""

    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """registers a user via a form and handles the form submission"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)
        # what is the .register? I assume it's a method name or something like that? 

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)
        # I noticed that the solution code doesn't put a / at the start of the URL when it's render template, but does when it's a redirect - is that important or no?

@app.route('/login', methods=["GET", "POST"])
def login():
    """provides form for user to login and handles submission of the form"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        # how does the .authenticate work? similar to my question above about User.register

        if user: 
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username and/or password"]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    """logs a user out"""

    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):
    """page user sees upon logging in"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
        # where is Unauthorized() coming from? i'm sure it raises an error that tells the user they're unauthorized, but what exactly is happening?

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """deletes a user and redirects to login page"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    # why do we do both the session.delete and session.pop? what's the difference?

    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add feedback form and handle processing"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )
        # why do we need to do both the title = form.title.data and also the title=title block? also is it important that one uses space around the = sign and the other doesn't?

        db.session.commit(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
        # the function is showing a form to submit feedback. at the end, if the form doesn’t validate, we render the feedback/new.html template. how is the form showing up prior to that? it’s just form = FeedbackForm() and then if form.validate_on_submit().

    else:
        return render_template("feedback/new.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """allows user to update feedback form and handles processing it"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)
    # don't understand the obj=feedback thing 

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)
    # is feedback/edit a different form?

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """allows user to delete previously submitted feedback"""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        # I noticed this above as well, but we do feedback = Feedback...(feedback_id), then use that to pull feedback.username. Does that first line give us all the information from that iteration of the Feedback model (I forget the proper syntax for that)? I assume so, just wanted to check.
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")





