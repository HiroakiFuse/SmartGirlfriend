# -*- coding: utf-8 -*-
# 必要なモジュールの読み込み
from flask import Flask, jsonify,make_response,request,render_template
from gevent import pywsgi
import gevent
from geventwebsocket.handler import WebSocketHandler
from flask_sockets import Sockets
from gevent.event import AsyncResult

#event処理の設定
massage = AsyncResult()
# __name__は現在のファイルのモジュール名
app = Flask(__name__)
sockets = Sockets(app)
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain('cert.crt','server.pass.key')
#reqの初期化
@app.route('/')
def index():
	return render_template('index1.html')
@app.route('/shenron',methods=['POST'])
def post():
	req = request.json['queryResult']['parameters']['Target']
	#characterの分岐
	if req == 'character':
		custom = request.json['queryResult']['parameters']['Custom']
		color = request.json['queryResult']['parameters']['Color']
		cascol = req+','+custom+','+color
		massage.set(cascol)
		gevent.sleep(0)
		result = jsonify({"fulfillmentText": req})
		return make_response(result)
	else:
		result = jsonify({"fulfillmentText": req})
		return make_response(result)
#websocket側
@sockets.route('/shenron')
def ws(ws):
	if request.environ.get('wsgi.websocket'):
		ws = request.environ['wsgi.websocket']
		while True:
			gevent.sleep(2)
			ms=massage.get()
			if ms is not None:
				ws.send(ms)
				massage.set()
			else:
				ws.send("deffault")
		return ''
		#return render_template('index.html')
	# エラーハンドリングi
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

def main():
	app.debug = True
	server = pywsgi.WSGIServer(("0.0.0.0",8000), app,handler_class=WebSocketHandler)
	server.serve_forever()

gevent.joinall([
	gevent.spawn(post),
	gevent.spawn(ws),
	])
if __name__ == "__main__":
    main()
