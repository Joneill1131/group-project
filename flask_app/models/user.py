from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db = 'hiking'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Creating new users
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW())"
        return connectToMySQL(cls.db).query_db(query,data)


    # getting all users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users


    #getting user by id
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    #getting user by email
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    #getting users who likes same trail
    @classmethod
    def get_users_like_same_trail(cls,data):
        query = "SELECT * FROM user_likes_trail JOIN users ON user_id = users.id JOIN trails ON trail_id= trails.id WHERE trail_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        all_users = []
        for users in results:
            all_users.append(cls(users))
        return all_users

    #  validation for register
    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.","register")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters.","register")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address.","register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.","register")
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords do not match!","register")
        return is_valid


    # validation for login
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['email']) == 0:
            is_valid = False
            flash('An email is required','login')
        if len(user['password']) == 0:
            is_valid = False
            flash('A password is required','login')
        return is_valid