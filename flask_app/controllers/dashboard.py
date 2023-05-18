from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.blog import Blog
from flask_app.models.like import Like


@app.route('/home')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        'id': session['user_id']
    }
    user = User.get_with_id(data)
    blogs = Blog.all_blogs()
    return render_template('home.html', user = user, blogs = blogs)