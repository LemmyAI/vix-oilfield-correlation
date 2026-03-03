#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Test</h1><p>If you see this, Flask works!</p>'

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
