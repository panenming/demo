import win32api
import win32con
import time
from bottle import request,Bottle,abort

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

app = Bottle()
@app.route('websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400,'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
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

server = WSGIServer(("127.0.0.1",9001),app,handler_class=WebSocketHandler)
server.serve_forever()

