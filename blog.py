import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
	'''This function creates a connection to the database and returns it'''
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row # provide access to the columns of the table by their names
	return conn

def get_post(id):
	''' Returns the post that matches with the given id or 404 not found. '''
	conn = get_db_connection()
	post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()
	conn.close()

	if post is None:
		abort(404)

	return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3@JD)ZwrnQq4sF86' # This is an arbitrary string.

@app.route('/')
def index():
	conn = get_db_connection()
	posts = conn.execute('SELECT * FROM posts').fetchall()
	conn.close()
	return render_template('index.html', posts=posts)

@app.route('/<int:id>')
def post(id):
	post = get_post(id)
	return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
	error = ''
	
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		if not title:
			error = 'Please fill in the title field !'
			flash('The title is required !')
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO posts(title, content) VALUES(?,?)', (title, content))
			conn.commit()
			conn.close()
			return redirect(url_for('index'))

	return render_template('create.html', error = error)

@app.route('/<int:id>/edit', methods = ('GET', 'POST'))
def edit(id):
	post = get_post(id)

	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		if not title:
			flash('The title is required !')
		else:
			conn = get_db_connection()
			conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
			conn.commit()
			conn.close()
			return redirect(url_for('index'))

	return render_template('edit.html', post = post)

@app.route('/<int:id>/delete', methods = ('POST',)) # Only post method is accepted
def delete(id):
	post = get_post(id)

	conn = get_db_connection()
	conn.execute('DELETE FROM posts WHERE id = ?', (id,))
	conn.commit()
	conn.close

	flash('"{}" was successfully deleted.'.format(post['title']))

	return redirect(url_for('index'))


