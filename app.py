from flask import Flask, render_template,jsonify

app = Flask(__name__)
HOST = '127.0.0.1'
PORT = '3000'

JOBS = [
    {
        'id': 1,
        'title': 'Data analyst',
        'salary': 'Rs 10,00,000',
        'location': 'Delhi'
    },
    {
        'id': 2,
        'title': 'Data scientist',
        'salary': 'Rs 12,00,000',
        'location': 'Banglore'
    },
    {
        'id': 3,
        'title': 'Backend engineer',
        'salary': 'Rs 15,00,000',
        'location': 'Chennai'
    },
    {
        'id': 4,
        'title': 'Frontend enginee',
        'salary': 'Rs 14,00,000,',
        'location': 'Kolkata'
    }
]


@app.route('/')  # root route
def hello_world():
    return render_template('home.html', jobs=JOBS, heading='Whats up')

@app.route('/api/jobs') # static route
def list_jobs():
    return jsonify(JOBS)

@app.route('/about/<username>') # dynamic route
def about_page(username):
    return f'<h4>This is about page of {username}</h4>'




if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
