from flask import Flask
from flask.templating import render_template
from flaskext.markdown import Markdown
import podcastindex
from flask import request
from werkzeug.datastructures import ContentSecurityPolicy
import os
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)
Markdown(app)


config = {
    "api_key": os.environ.get('KEY'),
    "api_secret": os.environ.get('SECRET')
}

# result = index.search("Tim Dillon Show",clean=True)["feeds"][0]['url']
# episodes=index.episodesByFeedUrl(result)['items'][0]['enclosureUrl']
# print(episodes)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        print(request.form['searchpodcast'])


    return render_template('index.html')

@app.route('/podcast/<id>',methods=['GET','POST'])
def podcast(id):
    index = podcastindex.init(config)
    results = index.episodesByFeedId(522613)['items']
    arr=[]
    for item in results:
        arr.append(item['enclosureUrl'])
    return render_template('podcastlist.html',list=arr)


