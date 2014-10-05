# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, g
from flask_flatpages import FlatPages
from flask_markdown import markdown
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin
import requests

app = Flask(__name__)
app.config['LANGUAGES'] = {
    'en': 'English',
    'es': 'Español',
    'ca': 'Català',
    'gl': 'Galego',
    'eu': 'Euskara'
}
app.secret_key = "SECRETKEY"

pages = FlatPages(app)

from flask.ext.babel import Babel
babel = Babel(app)
markdown(app)

@babel.localeselector
def get_locale():
    available_langs = app.config["LANGUAGES"].keys()
    default_lang = request.accept_languages.best_match(available_langs)
    res = request.args.get('lang', default_lang)
    if res not in available_langs:
        res = default_lang
    return res

@app.before_request
def before_request():
    g.locale = get_locale()
    g.available_langs = app.config["LANGUAGES"].keys()

@app.route('/blog/', methods=['GET'])
@app.route('/blog/<language>/', methods=['GET'])
@app.route('/blog/<language>/<post_id>')
def blog(language="es", post_id=False):
    language = language or g.locale
    if not post_id:
        articles = sorted((p for p in pages if (p.meta['language'] == language)),
            key=lambda p: p.meta['published'], reverse=True)
        single = False
    else:
        articles = sorted((p for p in pages if (p.meta['language'] == language and p.meta['post_id'] == post_id )),
            key=lambda p: p.meta['published'], reverse=True)
        single = True
    return render_template('blog.html', pages=articles, single=single)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/info', methods=['GET'])
def info():
    return render_template('informacion.html')

@app.route('/talks', methods=['GET'])
def talks():
    trello_talks = requests.get('https://api.trello.com/1/lists/53a70c099f3ce8897416347b/cards')
    trello_light = requests.get('https://api.trello.com/1/lists/53d038a3f52787e522bb6a74/cards')
    trello_wshop = requests.get('https://api.trello.com/1/lists/5412f25f85af556ea8c1e06b/cards')
    return render_template(
        'charlas.html',
        trello_talks = trello_talks.json(),
        trello_light = trello_light.json(),
        trello_wshop = trello_wshop.json(),
        total_talks = sorted(trello_talks.json() + trello_light.json() + trello_wshop.json(), key=lambda talk: len(talk['idMembersVoted']), reverse=True),
        trello_speakers_talks = set([talk['name'] for talk in trello_talks.json()]),
        trello_speakers_wshop = set([talk['name'] for talk in trello_wshop.json()]),
        trello_speakers_light = set([talk['name'] for talk in trello_light.json()]),
    )

def make_external(url):
        return urljoin(request.url_root, url)


@app.route('/recent.atom')
def blogfeed():
    feed = AtomFeed('Articulos Recientes', feed_url=request.url, url=request.url_root)
    for article in pages:
        if article.meta['published']:
            feed.add(
                article.meta['title'],
                article.html,
                author = article.meta['author'],
                url = urljoin(request.url_root, "/blog/" + article.meta['language']+ "/" + article.meta['post_id']),
                published = article.meta['published'],
                updated = article.meta['published']
            )

    return feed.get_response()

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022, debug=True)

if __name__ == "__main__":
    server()
