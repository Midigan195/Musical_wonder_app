#!/usr/bin/python3
""" This application opens both web pages for the site """
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def open_homepage():
    """ This route returns the homepage """
    return render_template('index.html')


@app.route('/anime.html')
def anime():
    """ This returns the anime page """
    anime_id = request.args.get('anime_id')
    return render_template('anime.html', anime_id=anime_id)


if __name__ == '__main__':
    app.run()
