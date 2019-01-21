# -*- coding: utf-8 -*-
# 必要なモジュールの読み込み
from flask import Flask, jsonify,make_response,request,render_template
from gevent import pywsgi
import gevent
from geventwebsocket.handler import WebSocketHandler
from time import sleep
# __name__は現在のファイルのモジュール名
app = Flask(__name__)
#reqの初期化
req = ''
aaa
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/shenron',methods=['POST'])
def post():
	global req
	req = request.json['queryResult']['parameters']['Target']
	
	#characterの分岐
	if req == 'character':
		custom = request.json['queryResult']['parameters']['Custom']
		color = request.json['queryResult']['parameters']['Color']
		cuscol = []
		cuscol.append(custom)
		cuscol.append(color)
		result = {"fulfillmentText":','}
		return make_response(jsonify(result))
	else:
		return make_response(jsonifyresult)
	
#websocket側
@app.route('/shenron')
def ws():
	global req
	if request.environ.get('wsgi.websocket'):
		print(request.environ.get('wsgi.websocket'))
		ws = request.environ['wsgi.websocket']
		while True:
			if req == '':
				ws.send('default')
				gevent.sleep(3)
			else:
				ws.send(req)
				gevent.sleep(3)
				req = ''
	return ''
		#return render_template('index.html')
	# エラーハンドリングi
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

def main():
	app.debug = True
	server = pywsgi.WSGIServer(("0.0.0.0", 5000), app,handler_class=WebSocketHandler)
	server.serve_forever()

if __name__ == "__main__":
    main()
