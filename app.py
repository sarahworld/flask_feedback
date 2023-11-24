from flask import Flask, render_template, redirect, session, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "Shh its asecret!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():

    return redirect("/register")

@app.route('/register', methods=['GET','POST'])
def register_page():

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email= form.email.data

        hashed_password = User.register(username,password)
        new_user = User(username=username, password=hashed_password.password, first_name=first_name, last_name=last_name, email=email )
  
        db.session.add(new_user);
        db.session.commit()
        session['username'] = new_user.username;

        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register_page.html', page_title='Register Page', form=form)



@app.route('/users/<string:username>')
def secret_page(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.filter_by(username=username).first();
    feedbacks = Feedback.query.filter_by(username=username).all();

    return render_template('secret.html',page_title='Secret Page', user = user, feedbacks=feedbacks)

@app.route('/login', methods=['GET','POST'])
def login_page():

    if "username" in session:
        return redirect(f"/users/{session['username']}")
         
    
    form = LoginForm()

    if form.validate_on_submit:
        username = form.username.data
        password = form.password.data

    login_user = User.authenticate(username, password)
   
    if login_user:
      
        session['username'] = login_user.username;
        return redirect(f'/users/{login_user.username}')
    else:
        form.username.errors = ['invalid username/password.'] 
    

    return render_template('login.html', page_title="Login Page", form=form)

@app.route('/logout')
def logout():
    
    session.pop('username');

    return redirect('/')

@app.route('/users/<string:username>/delete')
def delete_user(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    feedbacks = Feedback.query.filter_by(username=username).delete();
    user = User.query.filter_by(username=username).delete();

    db.session.commit();

    session.pop('user_id');
    return redirect('/')
    

@app.route('/users/<string:username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.filter_by(username=username).first();
    form = FeedbackForm()

    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback);
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('add_feedback.html', form=form, user=user)
    

@app.route('/users/<string:username>/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(username,feedback_id):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    feedback = Feedback.query.filter_by(id=feedback_id).first();
    user = User.query.filter_by(username=username);
    
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title=form.title.data
        feedback.content=form.content.data

        db.session.add(feedback);
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return render_template('update_feedback.html', form=form, user=user)


@app.route('/users/<string:username>/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(username,feedback_id):

    

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    feedback = Feedback.query.filter_by(id=feedback_id).delete();

    db.session.commit();

    return redirect(f'/users/{username}')