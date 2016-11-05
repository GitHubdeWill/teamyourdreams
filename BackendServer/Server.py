'''
Created on Nov 4, 2016

@author: kelvinzhang
'''
import os

from flask import Flask
from flask import send_from_directory


app = Flask(__name__)

@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('/', path);

if __name__ == '__main__':
    os.chdir('..')
    app.run(host='0.0.0.0', port='80')