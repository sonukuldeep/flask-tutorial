from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for
from os import path
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# create the extension
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.title} - {self.desc}'


HOST = '127.0.0.1'
PORT = '3000'

# run only once
# with app.app_context():
#     db.create_all()


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
    # return f'user {sno} deleted'
    return redirect(url_for("home_page"))

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        todo = db.get_or_404(Todo, sno)



@app.route('/show')  # static route
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'


@app.route('/about/<username>')  # dynamic route
def about_page(username):
    return f'<h4>This is about page of {username}</h4>'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
