from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import jwt

app = Flask(__name__)

mysql = MySQL()

#### APP MYSQL CONFIG
app.config['MYSQL_DATABASE_USER'] = 'sql12258580'
app.config['MYSQL_DATABASE_PASSWORD'] = 'IplvI8LUFY'
app.config['MYSQL_DATABASE_DB'] = 'sql12258580'
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net'

app.config['SECRET_KEY'] = 'secret'

mysql.init_app(app)
connection = mysql.connect()

def auth(usr,pwd):
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM User WHERE username='" + usr + "' and password='" + pwd + "'")
	data = cursor.fetchone()
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
	# try:
		#GATHER ALL DATA + CHECK TOKEN
	token = request.headers['token']
	send = jwt.decode(token, app.config['SECRET_KEY'])
	user = send["user"]
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM User WHERE username='" + user + "'")
	data = cursor.fetchone()
	send["first"] = data[3] #gather Firstname
	send["last"] = data[4]	#gather Lastname
	cursor.execute("SELECT * FROM announce")
	anc = cursor.fetchall()
	# except:
		# return jsonify({"error":"authen error"})
	return jsonify({"user":send,"announce":anc})

if __name__ == '__main__':
	app.run(debug=True)