# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort
from flask_flatpages import FlatPages

app = Flask(__name__)
pages = FlatPages(app)
app.secret_key = "SECRETKEY"

@app.route('/blog/', methods=['GET'])
@app.route('/blog', methods=['GET'])
@app.route('/blog/<language>', methods=['GET'])
def blog(language="es"):
    articles = sorted((p for p in pages if 'published' in p.meta and language in p.meta),
        key=lambda p: p.meta['published'])
    return render_template('blog.html', pages=articles)

@app.route('/<language>/', methods=['GET'])
@app.route('/', methods=['GET'])
def index(language="es"):
    if language in ["en", "es"]:
        return render_template('%s/index.html' %language)
    else:
        abort(404)

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022, debug=True)

if __name__ == "__main__":
    server()
