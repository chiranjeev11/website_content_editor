import pymysql

conn = pymysql.connect(
		host='localhost',
		user='chiranjeev', 
		password = "chints11#",
		db='project_awakinn',
		)

db = conn.cursor()
