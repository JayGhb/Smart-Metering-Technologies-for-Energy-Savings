from flask import Flask, jsonify, json, request
import MySQLdb
import datetime
#from flask_restful import Resource, Api
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine


#declare that our app is a WSGI (Web Server Gateway Interface) app
app = Flask(__name__)

#Connect to db
db = MySQLdb.connect(#host="localhost",
                     user="root",
                     #port=3306,
                     passwd="",
                     db="testDB",
                     unix_socket="/opt/lampp/var/mysql/mysql.sock")


cursor = db.cursor() #initialize cursor


def construct_json(tbl,result):
	'''Prepare data to be displayed in JSON format

	This module prepares data to be formated in JSON
	according to the table name passed as argument.
	Matches dictionary keys, representing database
	column names, to their appropriate values passed
	in the result array parameter.

	:type tbl: string
	:param tbl: the name of the database table

	:type result: 2D array
	:param result: the array returned from cursor.fetchall()

	:returns: a list with the constructed dictionary
	'''

	data = []

	if tbl=="LivingRoomTemp":
		for i in range(0,len(result)):
			temp_data={
				'id' : result[i][0],
				'room' : result[i][1],
				'temperature' : result[i][2],
				'scale' : result[i][3],
				'date' : result[i][4]
			}
			data.append(temp_data)
	elif tbl=="VRMS":
		for i in range(0,len(result)):
			temp_data={
				'id' : result[i][0],
				'topic' : result[i][1],
				'value' : result[i][2],
				'date' : result[i][3]
			}
			data.append(temp_data)
	return data



@app.route('/all/<table>')
def get_all(table):
	'''Construct "localhost:5000/all/<table>" url functionality.

	Executes appropriate sql query to return all entries in the
	corresponding table of the database in JSON format.
	Valid table names: "LivingRoomTemp", "VRMS"

	:type table: string
	:param table: the table name given in the URL

	:returns: the query result set in JSON format
	'''

	try:
		cursor.execute("SELECT * FROM "+table)
	except Exception as e:
		return "Exception type: "+ str(e)
	result = cursor.fetchall()
	data = construct_json(table,result)
	return jsonify({'data' : data})


@app.route('/today/<table>')
def get_today(table):
	'''Construct "localhost:5000/today/<table>" URL functionality.

	Retrieves current date from Datetime module.
	Executes appropriate sql query to return entries in the
	corresponding table of the database with today's timestamp,
	in JSON format. Valid table names: "LivingRoomTemp", "VRMS".

	:type table: string
	:param table: the table name given in the URL

	:returns: the query result set in JSON format
	'''

	now = datetime.datetime.now() 
	rightnow = now.strftime("%Y-%m-%d") 
	rnow = rightnow+'%' #attach a  %  behind date for query purposes
	select_stmt = "SELECT * FROM " +table+ " WHERE timestamp LIKE %(test)s"
	try:
		cursor.execute(select_stmt, {'test': rnow})
	except Exception as e:
		return "Exception type: "+ str(e)

	result = cursor.fetchall()
	data = construct_json(table,result)
	return jsonify({'data' : data})


@app.route('/query/<table>')
def query(table):
	'''Construct "localhost:5000/query/<table>?startDate=value1&endDate=value2" URL
	functionality

	Retrieves dates given in the URL as parameters. Executes appropriate sql query
	to return entries in the corresponding table of the database, between the given
	dates. Input values in YYYY-MM-DD format. Valid table names: "LivingRoomTemp",
	"VRMS". Entries corresponding to second date are not returned.
	Uncomment commented parts to implement pagination.

	:type table: string
	:param table: the table name given in the URL

	:returns: the query result set in JSON format
	'''
	
	date1 = request.args.get('startDate')
	date2 = request.args.get('endDate')

	#page = request.args.get('page', default=1, type=int)
	#limit = request.args.get('limit',default = 5, type=int)

	#my_int = ((page-1)*limit)+1

	queryy="SELECT * FROM "+table+" WHERE timestamp BETWEEN %(d1)s AND %(d2)s" #AND id>="+str(my_int)+" LIMIT "+str(limit)

	try:
		cursor.execute(queryy,{'d1': date1, 'd2': date2})
	except Exception as e:
		return "Exception type: "+ str(e)
	result = cursor.fetchall()
	data = construct_json(table,result)
	return jsonify({'data' : data})


@app.route('/paginate/<table>')
def return_all(table):
	'''Implements pagination. Construct "localhost:5000/paginate/<table> URL functionality

	Executes appropriate sql query to return all entries in the corresponding
	table of the database, paginated. Pass "limit=.." & "page=.." parameters
	in URL to change the defaults and navigate through pages. 
	Default values: limit=5, page=1

	:type table: string
	:param table: the table name given in the URL

	:returns: the query result set in JSON format
	'''

	page = request.args.get('page', default=1, type=int)
	limit = request.args.get('limit',default = 5, type=int)
	my_int = ((page-1)*limit)+1 #appropriate id number to appear first in each page

	try:
		cursor.execute("SELECT * FROM "+table+" WHERE id>="+str(my_int)+" LIMIT "+str(limit))
	except Exception as e:
		return "Exception type: "+ str(e)
	result = cursor.fetchall()
	data = construct_json(table,result)
	return jsonify({'data': data})


@app.route('/avg/<table>')
def avg_between_dates(table):
	'''Construct "localhost:5000/avg/<table>?date1=value1&date2=value2" URL functionality

	Retrieves dates given in the URL as parameters. Executes appropriate sql query
	to return the average value of in the corresponding table of the database,
	between the given dates. Input values in YYYY-MM-DD format. 
	Valid table names: "LivingRoomTemp", "VRMS".

	:type table: string
	:param table: the table name given in the URL

	:returns: the average value in JSON format. Value is either Temperature or VRMS
	measurement, depending on the table name provided.
	'''
	date1 = request.args.get('date1')
	date2 = request.args.get('date2')
	queryy="SELECT AVG(payload) FROM "+table+" WHERE timestamp BETWEEN %(d1)s AND %(d2)s"
	try:
		cursor.execute(queryy,{'d1': date1, 'd2': date2})
	except Exception as e:
		return "Exception type: "+ str(e)
	result = cursor.fetchall()
	data = []
	if table=="LivingRoomTemp":
		temp_data={
			'Temperature':result[0][0]
		}
	elif table=="VRMS":
		temp_data={
			'VRMS': result[0][0]
		}
	data.append(temp_data)

	return jsonify({'Average': data})


@app.route('/avg/today/<table>')
def avg_today(table):
	'''Construct 'localhost:5000/avg/today/<table>' URL functionality.

	Retrieves current date from Datetime module.
	Executes appropriate sql query to return the average value of 
	the entries in the corresponding table of the database with 
	today's timestamp. Valid table names: "LivingRoomTemp", "VRMS".

	:type table: string
	:param table: the table name given in the URL

	:returns: the average value in JSON format. Value is either Temperature or VRMS
	measurement, depending on the table name provided.
	'''
	now = datetime.datetime.now() 
	rightnow = now.strftime("%Y-%m-%d")
	rnow = rightnow+'%' #attach a  %  behind date for query purposes
	select_stmt = "SELECT AVG(payload) FROM " +table+ " WHERE timestamp LIKE %(test)s"
	try:
		cursor.execute(select_stmt, {'test': rnow})
	except Exception as e:
		return "Exception type: "+ str(e)
	result = cursor.fetchall()
	data = []
	if table=="LivingRoomTemp":
		temp_data={
			'Temperature':result[0][0]
		}
	elif table=="VRMS":
		temp_data={
			'VRMS': result[0][0]
		}
	data.append(temp_data)

	return jsonify({'Average_today': data})


if __name__ == '__main__':
	app.run()
