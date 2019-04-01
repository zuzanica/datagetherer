from flask import Flask, jsonify, render_template
from app import app, db
import os

from app import vote
PORT=15550

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, threaded=True)
