import bottle
from bottle import route, run, url, static_file

@route('/')
def index():
    return '<h1>Hello Bottle!</h1>'


