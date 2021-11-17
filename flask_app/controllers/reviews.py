from flask import render_template,session,flash,redirect,request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trail import Trail
from flask_app.models.review import Review
import os,requests


@app.route('/trail/<int:trail_id>/add_reviews',methods=['post'])
def add_reviews(trail_id):
    if 'user_id' not in session:
        return redirect("/logout")
    data = {
            'content':request.form['content'],
            'user_id':session['user_id'],
            "trail_id":trail_id,
        }
    Review.save(data)
    return redirect(f'/trail/{trail_id}')

@app.route('/trail/<int:trail_id>/delete_reviews',methods=['post'])
def delete_reviews(trail_id):
    data = {
        'user_id':session['user_id'],
        "trail_id":trail_id
    }
    Review.destroy(data)
    return redirect(f'/trail/{trail_id}')