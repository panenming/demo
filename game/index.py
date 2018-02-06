from bottle import run,route,static_file

@route('/')
def index():
    return static_file('index.html','./')

@route('/resource/<filename>')
def staticFile(filename):
    return static_file(filename,'./resource')


run(host="127.0.0.1",port="9000")