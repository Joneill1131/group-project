from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from datetime import date

class Trail:
    db = 'hiking'

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.distance = data['distance']
        self.complete_date = data['complete_date']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None #this is going to be where the user object will be put later
        self.liker = [] # 



    @classmethod  #save query new trail
    def save(cls,data):
        query = "INSERT INTO trails (name, location, distance, complete_date,rating, user_id) VALUES (%(name)s,%(location)s,%(distance)s,%(complete_date)s,%(rating)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)



    @classmethod # get all from table trails, user who created trail, likers who like this trail
    def get_all_trail(cls):
        query ="select * from trails left join users on users.id = trails.user_id left join user_likes_trail on trails.id = user_likes_trail.trail_id left join users as liker on user_likes_trail.user_id = liker.id;"        #goal:  turn a list of dict into a list of objects with each trail object associated with a user object
        results =  connectToMySQL(cls.db).query_db(query) #list of dict
        all_trails = [] # list of objects
        for row in results:
            new_trail = True
            liker_data ={
                'id': row['liker.id'],
                'first_name': row['liker.first_name'],
                'last_name': row['liker.last_name'],
                'email': row['liker.email'],
                'password': row['liker.password'],
                'created_at': row['liker.created_at'],
                'updated_at': row['liker.updated_at'],
            }
            if len(all_trails)>0 and all_trails[len(all_trails)-1].id == row['id']:
                all_trails[len(all_trails)-1].liker.append(user.User(liker_data))
                new_trail = False
            if new_trail:
                # make a class instance of trail
                this_trail = cls(row)
                # make a data dict for the user
                user_info ={
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                # make a user instance 
                this_user = user.User(user_info)
                # add that user object to the trail attribute "user"
                this_trail.user = this_user
                if row['liker.id'] is not None:
                    this_trail.liker.append(user.User(liker_data))
                all_trails.append(this_trail)
                print(all_trails)
        return all_trails



    @classmethod  #get one trail by id
    def get_one(cls,data):
        query = "SELECT * FROM trails WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )



    @classmethod  #update trail
    def update(cls, data):
        query = "UPDATE trails SET name=%(name)s, location=%(location)s, distance=%(distance)s, complete_date=%(complete_date)s,rating=%(rating)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)



    @classmethod  #delete trails
    def destroy(cls,data):
        query = "DELETE FROM trails WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)



    @classmethod #get trails that relate to user
    def get_user_trails(cls,data):
        query = 'select * from trails left join users on trails.user_id = users.id where users.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        trails = []
        for trail in results:
            trails.append(cls(trail))
        return trails



    @classmethod
    def like_trail(cls,data):
        query = 'insert into user_likes_trail (user_id,trail_id) values(%(user_id)s, %(trail_id)s);'
        return connectToMySQL(cls.db).query_db(query,data)



    @classmethod
    def unlike_trail(cls,data):
        query = 'delete from user_likes_trail where trail_id=%(trail_id)s and user_id =%(user_id)s;'
        return connectToMySQL(cls.db).query_db(query,data)



    @classmethod
    def trails_user_liked(cls,data):
        trails_liked = []
        query = "SELECT trail_id FROM user_likes_trail JOIN users on users.id= user_id where user_id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        for result in results:
            trails_liked.append(result['trail_id'])
        return trails_liked



    #validation  for trail
    @staticmethod
    def validate_trail(trail):
        is_valid = True
        today = str(date.today())
        print(today)
        if len(trail['name']) < 3:
            is_valid = False
            flash("Trail name must be at least 3 characters","trail")
        if len(trail['location']) == '':
            is_valid = False
            flash("Location cannot blank","trail")
        if trail['complete_date'] ==  '':
            is_valid = False
            flash("Please enter a date","trail")
        if trail['complete_date'] < today:
            is_valid = False
            flash('Event day cannot be in the past','trail')
        return is_valid
