from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import jwt
from config import *

app = Flask(__name__)

mysql = MySQL()

#### APP MYSQL CONFIG

mysql.init_app(app)

def auth(usr,pwd):
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM User WHERE username='" + usr + "' and password='" + pwd + "'")
	data = cursor.fetchone()
	cursor.close()
	connection.close()
	if data is None:
		return jsonify({"status" : "denied"})
	token = jwt.encode({"user":usr}, app.config['SECRET_KEY'])
	return jsonify({"token" : token.decode("utf-8") })

@app.route('/api/login', methods=['POST'])
def login():
	#AUTHEN TOKEN - NO TIMEOUT
	data = request.json
	usr = data["user"]
	pwd = data["pass"]
	token = auth(usr,pwd)
	return token

@app.route('/api/token', methods=['POST'])
def tkauth():
	try:
		#GATHER ALL DATA + CHECK TOKEN
		token = request.headers['token']
		print(1);
		send = jwt.decode(token, app.config['SECRET_KEY'])
		print(2);
		user = send["user"]
		connection = mysql.connect()
		cursor = connection.cursor()
		print(3);
		cursor.execute("SELECT * FROM User WHERE username='" + user + "'")
		print(45)
		data = cursor.fetchone()
		print('')
		send["first"] = data[2] #gather Firstname
		send["last"] = data[3]	#gather Lastname
		print(4);
		cursor.execute("SELECT * FROM announce")
		anc = cursor.fetchall()
		print(5);
		cursor.close()
		connection.close()
		print(6);
	except:
		return jsonify({"error":"authen error"})
	return jsonify({"user":send,"announce":anc})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7000, debug=True)