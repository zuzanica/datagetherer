from flask import Flask, jsonify, render_template
from app import app, db
import os

from app import vote


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, threaded=True)
