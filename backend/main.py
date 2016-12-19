import bottle
from bottle import route, run, url, static_file

#route files
import routes
from Api import user
#serve the static folder
@route('/static/<path:path>')
def static_files(path):
    print(path)
    return static_file(path, root='../static')

#main application
if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)

app = bottle.default_app()


