#!/usr/bin/python3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/anime.html')
def anime():
    anime_id = request.args.get('anime_id')

    return render_template('anime.html', anime_id=anime_id)

if __name__ == '__main__':
    app.run()
