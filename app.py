from flask import Flask, render_template, request, url_for, flash, redirect, send_file, flash
import sqlite3
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'confidential-key-to-be-inserted'
app.config['UPLOAD_FOLDER'] = 'static/files/'
app.config['DOWNLOAD_FOLDER'] = 'static/files/'
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/display', methods = ['GET', 'POST'])
def display_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(filelink)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"r")
        content = file.read()   
        
    return render_template('content.html', content=content) 
    

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    return render_template('upload.html')

def download(input_link):
    content = "File added successfully!"
    req = requests.get(input_link)
    filename = req.url[input_link.rfind("/")+1:]
    if (os.path.exists(app.config['UPLOAD_FOLDER']+filename)):
        content = "File already exists. "
    
    with open(app.config['UPLOAD_FOLDER'] +filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
            return filename, content

# https://filesamples.com/samples/document/txt/sample3.txt
# https://filesamples.com/samples/document/pdf/sample3.pdf

def openfile(filename):
    path = open(app.config['UPLOAD_FOLDER'] + filename,"r")
    data = path.read()
    return data

@app.route('/uploadlink', methods = ['GET', 'POST'])
def uploadlink():
    if request.method == 'POST':    # submitted
        input_link = request.form["userinput"]
        print(input_link)
        filename, content = download(input_link)
        data = openfile(filename)
        return render_template('alert.html', data=data, content=content)
    else:
        return render_template('uploadlink.html')



