from flask import render_template, session,flash,redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trail import Trail
from flask_app.models.review import Review
import os,requests


@app.route('/trail/new') # route to create trail
def new_trail():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add_trail.html',user=User.get_by_id(data))


@app.route('/create/trail',methods=['POST'])  #create new trail
def create_trail():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Trail.validate_trail(request.form):
        return redirect('/trail/new')
    data = {
        "name": request.form["name"],
        "location": request.form['location'],
        "distance": request.form["distance"],
        "complete_date":request.form['complete_date'],
        "rating":request.form['rating'],
        "user_id": session["user_id"]
    }
    Trail.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>/trail') # route to edit trail
def edit_trail(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("change_trail_date.html",edit=Trail.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/<int:id>/trail',methods=['POST']) #update trail
def update_trail(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Trail.validate_trail(request.form):
        return redirect(f'/edit/{id}/trail')
    data = {
        "id": request.form['id'],
        "name": request.form["name"],
        "location": request.form["location"],
        "distance": request.form["distance"],
        "complete_date": request.form['complete_date'],
        "rating":request.form['rating']
    }
    Trail.update(data)
    return redirect('/dashboard')


@app.route('/trail/<int:id>')
def show_trail(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    all_users= User.get_users_like_same_trail(data)
    trail = Trail.get_one(data)
    user = User.get_by_id(user_data)
    print (trail)
    address = trail.location
    api_key = os.environ.get("API_KEY")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    map ={
            'lat': response.json()['results'][0]['geometry']['location']['lat'],
            'lng': response.json()['results'][0]['geometry']['location']['lng']
        }
    print(map)
    all_reviews = Review.get_trail_reviews(data)
    return render_template("trail_info.html",trail=trail,user=user,all_users=all_users,map=map,api_key=api_key,all_reviews=all_reviews)

@app.route('/trail/<int:trail_id>/like',methods = ['post'])
def like(trail_id):
    liker_data ={
        'user_id':session['user_id'],
        "trail_id":trail_id
    }
    Trail.like_trail(liker_data)
    return redirect('/dashboard')

@app.route('/trail/<int:trail_id>/unlike',methods = ['post'])
def unlike(trail_id):
    unliker_data ={
        'user_id':session['user_id'],
        "trail_id":trail_id
    }
    Trail.unlike_trail(unliker_data)
    return redirect('/dashboard')



@app.route('/delete/<int:id>/trail', methods = ['post']) #destroy trail
def destroy_trail(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Trail.destroy(data)
    return redirect('/dashboard')
