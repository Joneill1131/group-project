
from flask import render_template, session,redirect, request,flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trail import Trail
from flask_app.models.review import Review

bcrypt = Bcrypt(app)


@app.route('/') #get method, the home page
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])  #post method,, to register a new user
def register():
    is_valid = User.validate_register(request.form)
    if not is_valid:
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = User.save(new_user)
    session['user_id'] = id
    return redirect('/dashboard')


@app.route("/login",methods=['POST'])   #post method . to login 
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/dashboard')



@app.route('/dashboard')    #the dashboard to display all trails
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data),trails=Trail.get_all_trail(),trails_user_liked=Trail.trails_user_liked(data))



@app.route('/mytrails')  #the session[user] who created trails, edit and delete 
def mytrail():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id':session['user_id']
    }
    user = User.get_by_id(data)
    trails = Trail.get_user_trails(data)
    return render_template("all_trails.html",user = user,trails = trails)


@app.route('/logout') # logout
def logout():
    session.clear()
    return redirect('/')
