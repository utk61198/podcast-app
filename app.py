from email.mime import image
from flask import Flask
from flask.templating import render_template
from flaskext.markdown import Markdown
import podcastindex
from flask import request
from werkzeug.datastructures import ContentSecurityPolicy
import os
from dotenv import load_dotenv
from werkzeug.utils import redirect
load_dotenv()

app=Flask(__name__)
Markdown(app)


config = {
    "api_key": os.environ.get('KEY'),
    "api_secret": os.environ.get('SECRET')
}

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        print(request.form['searchpodcast'])
        index = podcastindex.init(config)
        results=index.search(request.form['searchpodcast'],clean=True)
        if results!=None:
            # feed_id=results['feeds'][0]['id']
            # return redirect("/podcast/"+str(feed_id))
            arr=[]
            for item in results['feeds']:
                fid="/podcast/"+str(item['id'])
                title=item['title']
                podcast_obj={
                    'title':title,
                    'feedid':fid
                }
                arr.append(podcast_obj)
            return render_template('index.html',searchresults=arr)
    return render_template('index.html',searchresults=[])


@app.route('/podcast/<feed_id>',methods=['GET','POST'])
def podcast(feed_id):
    index = podcastindex.init(config)
    results = index.episodesByFeedId(feed_id,max_results=100)['items']
    podcast_name = index.podcastByFeedId(feed_id)["feed"]["title"]
    print(index.podcastByFeedId(feed_id))
    podcast_description=index.podcastByFeedId(feed_id)["feed"]["description"]
    podcast_cover_image=index.podcastByFeedId(feed_id)["feed"]["image"]
    arr=[]
    for item in results:
        arr.append(item)
    return render_template('podcastlist.html',list=arr,name=podcast_name,description=podcast_description,image=podcast_cover_image)


