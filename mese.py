import os
import subprocess
from collections import OrderedDict
from flask import Flask
from flask import Response
from flask import render_template as flask_render_template
from flask import request
from werkzeug.datastructures import Headers
from api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')


def render_template(name, **kwargs):
    name = os.path.join('slim', name)
    is_slim = request.args.get('slim', False)
    if is_slim:
        return flask_render_template(name, **kwargs)
    return flask_render_template('complete.html', name=name, **kwargs)


@app.route('/')
def index():
    playlist = [
        {'href': 'http://localhost/tv/30%20Rock/30%20Rock%20-%207x01%20-%20The%20Beginning%20of%20the%20End.mkv', 'title': 'The Beginning of the End', 'type': 'video', 'details': OrderedDict([('Title', 'The Beginning of the End'), ('Episode', '01'), ('Season', '07'), ('Show', '30 Rock')])},
        {'href': 'http://localhost/music/Barenaked%20Ladies/Are%20Me/01%20Adrift.mp3', 'title': 'Adrift', 'type': 'audio', 'details': OrderedDict([('Title', 'Adrift'), ('Track', '01'), ('Album', 'Are Me'), ('Artist', 'Barenake Ladies')])}
    ]
    return render_template('index.html', playlist=playlist)


@app.route('/music/')
def music():
    return render_template('music.html')


@app.route('/tv/')
def tv():
    return render_template('tv.html')


@app.route('/movies/')
def movies():
    return render_template('movies.html')


@app.route('/settings/')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
