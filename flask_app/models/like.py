from flask_app.config.mysqlconnection import connectToMySQL

class Like:
    DB = 'blogs'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.blog_id = data['blog_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    @classmethod
    def add_likes(cls, data):
        query = """INSERT INTO likes (user_id, blog_id, created_at, updated_at)
                VALUES (%(user_id)s, %(blog_id)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def delete_like(cls, data):
        query = """DELETE FROM likes
                WHERE blog_id = %(blog_id)s AND user_id = %(user_id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def test_for_like(cls, data):
        query = """SELECT * FROM likes 
                LEFT JOIN users
                ON users.id = likes.user_id
                LEFT JOIN blogs
                ON likes.blog_id = blogs.id
                WHERE blogs.id = %(blog_id)s and users.id = %(user_id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])