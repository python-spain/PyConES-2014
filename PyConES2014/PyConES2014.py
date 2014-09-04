# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort
from flask_flatpages import FlatPages

app = Flask(__name__)
pages = FlatPages(app)
app.secret_key = "SECRETKEY"

@app.route('/blog/', methods=['GET'])
@app.route('/blog', methods=['GET'])
@app.route('/blog/<language>', methods=['GET'])
@app.route('/blog/<language>/<post_id>')
def blog(language="es", post_id=False):
    if not post_id:
        articles = sorted((p for p in pages if (p.meta['language'] == language)),
            key=lambda p: p.meta['published'], reverse=True)
        single = False
    else:
        articles = sorted((p for p in pages if (p.meta['language'] == language and p.meta['post_id'] == post_id )),
            key=lambda p: p.meta['published'], reverse=True)
        single = True
    return render_template('blog.html', pages=articles, single=single)

@app.route('/<language>/', methods=['GET'])
@app.route('/', methods=['GET'])
def index(language="es"):
    print "index"
    if language in ["en", "es"]:
        return render_template('%s/index.html' %language)
    else:
        abort(404)

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022, debug=True)

if __name__ == "__main__":
    server()
