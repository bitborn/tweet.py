import os
from flask import *
from datetime import datetime
from peewee import *
import pw_database_url
from flask_peewee.db import Database


DATABASE = pw_database_url.config()
DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask('tweet')
app.config.from_object(__name__)

db = Database(app)

class Tweet(db.Model):
    """
    The data type for a tweet
    """
    created = DateTimeField()
    content = TextField()

    class Meta:
        order_by = ('-created',)


@app.template_filter('strftime')
def strftime(date):
        return date.strftime('%a, %b %d, %Y %I %p')

@app.route('/', methods=['GET'])
def index():
    query = Tweet.select(Tweet.id, Tweet.created, Tweet.content)
    tweets = list(query)
    return render_template('index.html', tweets=tweets)

@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html')

@app.route('/', methods=['POST'])
def create():
    content = request.form.get('content', None)
    if content and len(content) <= 140:
        tweet = Tweet.create(
            content = content,
            created = datetime.now()
        )
        return redirect(url_for('index'))
    else:
        return redirect(url_for('new'))
    

if __name__ == '__main__':
    app.debug = True
    Tweet.create_table(fail_silently=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
