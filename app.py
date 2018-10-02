from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import jwt

app = Flask(__name__)

mysql = MySQL()

#### APP MYSQL CONFIG

app.config['SECRET_KEY'] = 'secret'

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

@app.route('/login', methods=['POST'])
def login():
	#AUTHEN TOKEN - NO TIMEOUT
	data = request.json
	usr = data["user"]
	pwd = data["pass"]
	token = auth(usr,pwd)
	return token

@app.route('/token', methods=['POST'])
def tkauth():
	try:
		#GATHER ALL DATA + CHECK TOKEN
		token = request.headers['token']
		send = jwt.decode(token, app.config['SECRET_KEY'])
		user = send["user"]
		connection = mysql.connect()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM User WHERE username='" + user + "'")
		data = cursor.fetchone()
		send["first"] = data[3] #gather Firstname
		send["last"] = data[4]	#gather Lastname
		cursor.execute("SELECT * FROM announce")
		anc = cursor.fetchall()
		cursor.close()
		connection.close()
	except:
		return jsonify({"error":"authen error"})
	return jsonify({"user":send,"announce":anc})

if __name__ == '__main__':
	app.run(debug=True)