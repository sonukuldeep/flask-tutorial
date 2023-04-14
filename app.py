from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for
from os import path
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create the app
app = Flask(__name__)
# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

HOST = '127.0.0.1'
PORT = '3000'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f'User {self.username} - {self.email}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f'Post {self.title} - {self.date_posted}'


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.title} - {self.desc}'


#run only once
# with app.app_context():
#     db.create_all()

@app.route('/create-user')
def create_user():
    # Add a new user to the database
    new_user = User(username='JohnDoe', email='johndoe@example.com', password='password')
    db.session.add(new_user)
    db.session.commit()

    # Add a new post associated with the user to the database
    new_post = Post(title='First Post', content='Hello World!', user_id=new_user.id)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])  # root route
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('home.html', allTodo=allTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = db.get_or_404(Todo, sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home_page"))

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = db.get_or_404(Todo, sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("home_page"))

    return render_template('update.html', todo=todo)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == '__main__':
   app.run(host=HOST, port=PORT, debug=True)
