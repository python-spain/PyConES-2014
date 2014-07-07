from flask import Flask, render_template, abort, Response, request, redirect, flash, url_for
import Digenpy_, json
from Digenpy_ import *
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "SECRETKEY"

@app.route('/en/', methods=['GET'])
def indexen():
    return render_template('index.en.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/cfp', methods=['GET'])
def cfp():
    return render_template('cfp.html')

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022)

if __name__ == "__main__":
    server()
