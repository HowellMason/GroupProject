from flask_app import app
from flask import redirect, request, session
from flask_app.models.user import User
from flask_app.models.blog import Blog
from flask_app.models.like import Like

@app.route('/blog/like/<int:blog_id>/<int:user_id>')
def process_like(blog_id, user_id):
    data = {
        'blog_id': blog_id,
        'user_id': user_id
    }
    if not Like.test_for_like(data):
        Like.add_likes(data)
    else:
        Like.delete_like(data)
    return redirect('/home')
