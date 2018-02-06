import win32api
import win32con
import time
import threading
from bottle import request, Bottle, abort, static_file
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent import monkey

monkey.patch_all()

app = Bottle()
@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
            message = wsock.receive()
            print(message)
            if message == 'reload':
                win32api.keybd_event(82, 0, 0, 0)
                time.sleep(0.1)
                win32api.keybd_event(82, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif message == 'shoot_start':
                win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(32, 0, 0, 0)
            elif message == 'shoot_end':
                time.sleep(0.1)
                win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif message == 'leftward':
                win32api.keybd_event(37, 0, 0, 0)
                time.sleep(0.1)
                win32api.keybd_event(37, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif message == 'rightward':
                win32api.keybd_event(39, 0, 0, 0)
                time.sleep(0.1)
                win32api.keybd_event(39, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif message == 'forward':
                win32api.keybd_event(38, 0, 0, 0)
                time.sleep(0.1)
                win32api.keybd_event(38, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif message == 'backward':
                win32api.keybd_event(40, 0, 0, 0)
                time.sleep(0.1)
                win32api.keybd_event(40, 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                wsock.send(message)
            wsock.send('reset')
        except WebSocketError:
            break

server = WSGIServer(("0.0.0.0", 9001), app, handler_class=WebSocketHandler)

def websocket():
    global server
    server.serve_forever()
thread1 = threading.Thread(target=websocket)
thread1.start()

app2 = Bottle()
@app2.route('/')
def index():
    return static_file('index.html', 'game')

@app2.route('/resource/<filename>')
def staticFile(filename):
    return static_file(filename, 'game/resource')

app2.run(host='0.0.0.0', port='9000')
