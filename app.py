from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from flask import g

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = setupDb()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.connect().close()

def setupDb():
	mysql = MySQL()
	 
	# MySQL configurations
	app.config['MYSQL_DATABASE_USER'] = 'root'
	app.config['MYSQL_DATABASE_PASSWORD'] = 'nanivallu'
	app.config['MYSQL_DATABASE_DB'] = 'devathon'
	app.config['MYSQL_DATABASE_HOST'] = 'localhost'
	mysql.init_app(app)
	return mysql




def insertData(name, amount, tags,fromacc, toacc, type, transactiondate, mysql):
	
	conn = mysql.connect()
	cursor = conn.cursor()
	command = "INSERT INTO TRANSACTIONS (NAME, AMOUNT, TAGS, FROMACC, TOACC, TYPE, TRANSACTIONDATE ) VALUES ('{0}', '{1}','{2}','{3}','{4}','{5}','{6}')".format(name, amount, tags, fromacc, toacc, type, transactiondate)
	try:
		cursor.execute(command)
		conn.commit()
		print "success"
	except Exception as e:
		print e
		conn.rollback()
	data = cursor.fetchall()
	print data
	db_disconnect(conn)

@app.route('/submit',methods=['GET', 'POST'])
def submit():
	mysql = setupDb()
	if request.method == 'GET':
		#return ''
		print type(request)
		print dir(request)
		print request.form
		
		_amount = request.form.get('amount')
		_tags = request.form.get('tags')
		_name = request.form.get('name')
		_fromacc = request.form.get('account')
		_toacc = request.form.get('account2')
		_type = request.form.get('type')
		_date = request.form.get('date')


		print  _name, _amount, _tags, _fromacc, _toacc, _type, _date
		if _amount and _type:
			insertData(_name, _amount, _tags, _fromacc, _toacc, _type, _date, mysql)
		return render_template('checkingapp.html')
	else:
		_amount = request.form.get('amount')
		_tags = request.form.get('tags')
		_name = request.form.get('name')
		_fromacc = request.form.get('account')
		_toacc = request.form.get('account2')
		_type = request.form.get('type')
		_date = request.form.get('date')


		print  _name, _amount, _tags, _fromacc, _toacc, _type, _date
		if _amount and _type:
			print "inserting..."
			insertData(_name, _amount, _tags, _fromacc, _toacc, _type, _date, mysql)
			print "inserted..."
			return render_template('index.html')
	

	
@app.route("/")
def main():
    return render_template('index.html')
	
if __name__ == "__main__":
    app.run()

