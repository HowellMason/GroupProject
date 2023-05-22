from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import like
from flask import flash

class Blog:
    DB = 'blogs'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.likes = []
    @staticmethod
    def validate_blog(blog):
        is_valid = True
        if ((len(blog['title'])) - (blog['title'].count(' ')) == 0) and ((len(blog['content'])) - (blog['content'].count(' ')) == 0):
            flash("All fields required")
            is_valid = False
# ----- BLOG TITLE VALIDATIONS
        elif len(blog['title']) - (blog['title'].count(' ')) == 0:
            flash("Blog title is required")
            is_valid = False
        elif len(blog['title']) - (blog['title'].count(' ')) < 2:
            flash("Blog title must be atleast 2 characters")
            is_valid = False
        elif len(blog['title']) > 100:
            flash("Blog title must less than 100 character")
            is_valid = False
# ----- BLOG CONTENT VALIDATIONS
        elif len(blog['content']) - (blog['content'].count(' ')) == 0:
            flash("Blog content is required")
            is_valid = False
        elif len(blog['content']) - (blog['content'].count(' ')) < 2:
            flash("Blog content must be atleast 2 characters")
            is_valid = False
        elif len(blog['content']) > 2500:
            flash("Blog content must be less than 2500 characters")
            is_valid = False
        return is_valid
    @classmethod
    def new_blog(cls, data):
        query = """INSERT INTO blogs (title, content, user_id, created_at, updated_at)
                VALUES (%(title)s, %(content)s, %(user_id)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def all_blogs(cls):
        query = """SELECT * FROM blogs 
            LEFT JOIN users
            ON blogs.user_id = users.id
            LEFT JOIN likes AS likes
            ON likes.blog_id = blogs.id
            LEFT JOIN users AS liker
            ON liker.id = likes.user_id
            ORDER BY blogs.created_at DESC;"""
        results = connectToMySQL(cls.DB).query_db(query)
        all_blogs = []
        for blog in results:
            print(results[0].keys())
            if len(all_blogs) == 0 or this_blog.id != blog['id']:
                this_blog = cls(blog)
                this_blog.creator = user.User({
                    'id': blog['users.id'],
                    'first_name': blog["first_name"],
                    'last_name': blog["last_name"],
                    'email': blog["email"],
                    'password': blog["password"],
                    'created_at': blog["users.created_at"],
                    'updated_at': blog["users.updated_at"]
                })
                all_blogs.append(this_blog)
            if blog['likes.id'] != None:
                this_like = like.Like({
                    'id': blog['likes.id'],
                    'user_id': blog['likes.user_id'],
                    'blog_id': blog['blog_id'],
                    'created_at': blog['likes.created_at'],
                    'updated_at': blog['likes.updated_at']
                })
                this_like.creator = user.User({
                    'id': blog['liker.id'],
                    'first_name': blog["liker.first_name"],
                    'last_name': blog["liker.last_name"],
                    'email': blog["liker.email"],
                    'password': '',
                    'created_at': blog["liker.created_at"],
                    'updated_at': blog["liker.updated_at"]
                })
                this_blog.likes.append(this_like)
        return all_blogs
    @classmethod
    def get_with_id(cls, data):
        query = """SELECT * FROM blogs 
                LEFT JOIN users 
                ON blogs.user_id = users.id
                LEFT JOIN likes AS likes
                ON blogs.id = likes.blog_id
                LEFT JOIN users AS liker
                ON likes.user_id = liker.id
                WHERE blogs.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        one_blog = []
        for blog in results:
            if len(one_blog) == 0 or one_blog.id != blog['id']:
                this_blog = cls(blog)
                this_blog.creator = user.User({
                    'id': blog['users.id'],
                    "first_name": blog["first_name"],
                    "last_name": blog["last_name"],
                    "email": blog["email"],
                    "password": blog["password"],
                    "created_at": blog["users.created_at"],
                    "updated_at": blog["users.updated_at"]
                })
                one_blog.append(this_blog)
            if blog['likes.id'] != None:
                this_like = like.Like({
                    'id': blog['likes.id'],
                    'user_id': blog['likes.user_id'],
                    'blog_id': blog['likes.blog_id'],
                    'created_at': blog['likes.created_at'],
                    'updated_at': blog['likes.updated_at']
                })
                this_like.creator = user.User({
                        'id': blog['liker.id'],
                        'first_name': blog["liker.first_name"],
                        'last_name': blog["liker.last_name"],
                        'email': blog["liker.email"],
                        'password': '',
                        'created_at': blog["liker.created_at"],
                        'updated_at': blog["liker.updated_at"]
                    })
                this_blog.likes.append(this_like)
        return one_blog
    @classmethod
    def users_blogs(cls, data):
        query = """SELECT * FROM blogs
                LEFT JOIN users
                ON users.id = blogs.user_id
                LEFT JOIN likes AS likes
                ON likes.blog_id = blogs.id
                WHERE users.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        users_blogs = []
        for blog in results:
            if len(users_blogs) == 0 or users_blogs.id != blog['id']:
                this_blog = cls(blog)
                this_blog.creator = user.User({
                    'id': blog['users.id'],
                    "first_name": blog["first_name"],
                    "last_name": blog["last_name"],
                    "email": blog["email"],
                    "password": blog["password"],
                    "created_at": blog["users.created_at"],
                    "updated_at": blog["users.updated_at"]
                })
                users_blogs.append(this_blog)
            if blog['likes.id'] != None:
                this_like = like.Like({
                    'id': blog['likes.id'],
                    'user_id': blog['likes.user_id'],
                    'blog_id': blog['likes.blog_id'],
                    'created_at': blog['likes.created_at'],
                    'updated_at': blog['likes.updated_at']
                })
                this_like.creator = user.User({
                        'id': blog['liker.id'],
                        'first_name': blog["liker.first_name"],
                        'last_name': blog["liker.last_name"],
                        'email': blog["liker.email"],
                        'password': '',
                        'created_at': blog["liker.created_at"],
                        'updated_at': blog["liker.updated_at"]
                    })
                this_blog.likes.append(this_like)
        return users_blogs
    @classmethod
    def edit_blog(cls, data):
        query = """UPDATE blogs
                SET title = %(title)s,
                content = %(content)s,
                updated_at = NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def delete_blog(cls, data):
        query = """DELETE FROM blogs 
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)