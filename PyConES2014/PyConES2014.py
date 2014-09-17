# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, g
from flask_flatpages import FlatPages
from flask_markdown import markdown
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

@app.route('/talks', methods=['GET'])
def talks():
    trello_talks = requests.get('https://api.trello.com/1/lists/53a70c099f3ce8897416347b/cards')
    trello_light = requests.get('https://api.trello.com/1/lists/538d8d3461b92467e2686d3a/cards')
    trello_wshop = requests.get('https://api.trello.com/1/lists/5412f25f85af556ea8c1e06b/cards')
    return render_template(
        'charlas.html',
        trello_talks = sorted(trello_talks.json(), key=lambda talk: len(talk['idMembersVoted'])),
        trello_light = trello_light.json(),
        trello_wshop = trello_wshop.json()
    )

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022, debug=True)

if __name__ == "__main__":
    server()
