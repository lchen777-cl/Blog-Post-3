# export FLASK_ENV=development
# flask run

from flask import Flask, g, render_template, request

import sqlite3, string

app = Flask(__name__)

@app.route('/')
def main():
	return render_template("main.html")

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
	if request.method == 'GET':
		return render_template('submit.html')
	elif request.method == 'POST':
		insert_message(request)
		return render_template('submit.html')
	else:
		try:
			return render_template('submit.html', message=request.form['message'], name=request.form['name'])
		except:
			return render_template('submit.html')

@app.route('/view/', methods=['POST', 'GET'])
def view():
	return render_template('view.html', results = random_messages(3))

# create database for message
def get_message_db():
	#check whether the database message_db exists
	if 'message_db' not in g:
		# if not connect to the databse
		g.message_db = sqlite3.connect("messages_db.sqlite")
		c = g.message_db.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS messages (id integer, handle text, message text)''')
		#commit the changes to db
		g.message_db.commit()

	return g.message_db

def insert_message(request):
	message = request.form['message']
	name = request.form['name']
	db = get_message_db()
	cursor = db.cursor()
	cursor.execute("select count(*) from messages")
	count = cursor.fetchone()[0] + 1
	db.commit()
	db.execute(
				'INSERT INTO messages (id, handle, message) VALUES (?, ?, ?)',
				(count, name, message)
	)
	db.commit()
	return message, name

def random_messages(n):
	db = get_message_db()
	cursor = db.cursor()
	cursor.execute("select count(*) from messages")
	count = cursor.fetchone()[0]
	n = min(count, n)
	command = "SELECT * FROM messages ORDER BY RANDOM() LIMIT " + str(n)
	cursor.execute(command)
	s = ""
	for row in cursor:
		s = s + row[2] + "<br />" + "- <i>"+ row[1] + "</i><br />" + "<br />"
	#close the connection
	g.message_db.close()
	return s

