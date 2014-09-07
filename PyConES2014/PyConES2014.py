# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, g
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config['LANGUAGES'] = {
    'en': 'English',
    'es': 'Español'
}
app.secret_key = "SECRETKEY"

pages = FlatPages(app)

from flask.ext.babel import Babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    available_langs = app.config["LANGUAGES"].keys()
    default_lang = request.accept_languages.best_match(available_langs)
    res = request.args.get('lang', default_lang)
    app.logger.debug('Language: %s' % res)
    return res

@app.before_request
def before_request():
    g.locale = get_locale()

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

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022, debug=True)

if __name__ == "__main__":
    server()
