from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import search_worldcup
import search_world
import search_movie

app = Flask(__name__)
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
'''

'''
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
'''

@app.route('/', methods=['POST','GET'])
def index():
    return render_template('index.html')
    
@app.route('/search', methods = ['POST','GET'])
def search():
    words = request.form.get('words')
    database = request.form.get('database')
    if not words or not database:
        return '<br><h2 style="text-align: center">Failure. Please enter \
searching words and choose database.</h2>'
    if database == 'worldcup':
        result = search_worldcup.search(words)
        return render_template('result_worldcup.html', result = result)
    elif database == 'world':
        result = search_world.search(words)
        return render_template('result_world.html', result = result)
    elif database == 'movie':
        result = search_movie.search(words)
        return render_template('result_movie.html', result = result)


@app.route('/worldcup/<table>/<key>/<value>')
def worldcup_value(table, key, value):
    try:
        heap = search_worldcup.table_search(table, key, int(float(value)))
    except:
        heap = search_worldcup.table_search(table, key, value)
    return render_template('value_worldcup.html', table = table, heap = heap)

@app.route('/world/<table>/<key>/<value>')
def world_value(table, key, value):
    try:
        heap = search_world.table_search(table, key, int(float(value)))
    except:
        heap = search_world.table_search(table, key, value)
    return render_template('value_world.html', table = table, heap = heap)

@app.route('/movie/<table>/<key>/<value>')
def movie_value(table, key, value):
    try:
        heap = search_movie.table_search(table, key, int(float(value)))
    except:
        heap = search_movie.table_search(table, key, value)
    return render_template('value_movie.html', table = table, heap = heap)




if __name__ == "__main__":
    app.run(debug = True)
