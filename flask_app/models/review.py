from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models  import user,trail


class Review:
    db= 'hiking'

    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user  = None


    @classmethod
    def save(cls,data):
        query =  "INSERT INTO reviews(content,trail_id,user_id) values (%(content)s,%(trail_id)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod #get reviews that relate to trail
    def get_trail_reviews(cls,data):
        query = 'select * from reviews left join users on reviews.user_id = users.id where users.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        reviews = []
        for review in results:
            reviews.append(cls(review))
        return reviews


    @classmethod  #delete reviews
    def destroy(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
