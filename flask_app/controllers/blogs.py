from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.blog import Blog
from flask_app.models.like import Like
from flask_app.controllers import likes


# --- VIEW BLOGS

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

@app.route('/blogs/<int:blog_id>')
def view_blog(blog_id):
    data = {
        'id': blog_id
    }
    userinfo = {
        'id': session['user_id']
    }
    blog = Blog.get_with_id(data)
    user = User.get_with_id(userinfo)
    return render_template('viewblog.html', blog = blog, user = user)

@app.route('/my_blogs/<int:user_id>')
def view_my_blogs(user_id):
    data = {
        'id': user_id
    }
    userinfo = {
        'id': session['user_id']
    }
    blogs = Blog.users_blogs(data)
    user = User.get_with_id(userinfo)
    return render_template('myblogs.html', blogs = blogs, user = user)


# --- NEW BLOGS

@app.route('/blogs/new')
def new_blog():
    data = {
        'id': session['user_id']
    }
    user = User.get_with_id(data)
    return render_template('newblog.html', user = user)

@app.route('/blogs/new/process', methods = ['POST'])
def process_blog():
    if not Blog.validate_blog(request.form):
        return redirect('/blogs/new')
    data = {
        'title': request.form['title'],
        'content': request.form['content'],
        'user_id': request.form['user_id'],
    }
    Blog.new_blog(data)
    return redirect('/home')


# --- EDIT BLOGS

@app.route('/blogs/edit/<int:blog_id>')
def edit_blog(blog_id):
    data = {
        'id': blog_id
    }
    userinfo = {
        'id': session['user_id']
    }
    blog = Blog.get_with_id(data)
    user = User.get_with_id(userinfo)
    return render_template('editblog.html', user = user, blog = blog)

@app.route('/blogs/edit/process/<int:blog_id>', methods = ['POST'])
def process_edit(blog_id):
    if not Blog.validate_blog(request.form):
        return redirect('/blogs/edit/' + str(blog_id))
    data = {
        'id': blog_id,
        'title': request.form['title'],
        'content': request.form['content']
    }
    Blog.edit_blog(data)
    return redirect('/blogs/' + str(blog_id))


# --- DELETE BLOGS

@app.route('/blogs/destroy/<int:blog_id>')
def delete_blog(blog_id):
    data = {
        'id': blog_id
    }
    Blog.delete_blog(data)
    redirectlink = '/my_blogs/' + str(session['user_id']) 
    return redirect(redirectlink)