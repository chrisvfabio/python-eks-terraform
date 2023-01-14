#!/usr/bin/python

import os
import math

from flask import Flask
app = Flask(__name__)


VERSION = '1.0.0'

@app.route('/')
def hello():
    hostname = os.environ.get('HOSTNAME')
    version = VERSION

    # do some cpu intensive computation
    x = 0.0001
    for i in range(0, 1000000):
        x = x + math.sqrt(x)

    return 'HelloWorld version: {}, instance {}\n'.format(
        version,
        hostname
    )


@app.route('/health')
def health():
    return 'Helloworld is healthy', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True)
