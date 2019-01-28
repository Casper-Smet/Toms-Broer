import mysql.connector



def connect_database():
	database = mysql.connector.connect(
		host='145.89.166.209',
		user='tom',
		password='broer'
	)
	return database

def get_PoI():
	try:
		database = connect_database()
		cursor = database.cursor()

		cursor.execute('use tomsbroer;')
		cursor.execute('select * from points_of_interest order by searched desc;')

		data = []

		for x in cursor:
			temp = dict()

			temp['ID'] = x[0]
			temp['Name'] = x[1]
			temp['coordinates'] = x[2]
			temp['searched'] = x[3]

			data.append(temp)
	except:
		get_PoI()

	print(data[:3])
	return data[:3]

def one_upper():
	poi_id = 1
	update = "UPDATE points_of_interest SET searched = searched + 1 WHERE ID =" + str(poi_id)+ ";"
	try:
		database = connect_database()
		cursor = database.cursor()

		cursor.execute('use tomsbroer;')
		cursor.execute(update)
	except:
		one_upper()
#get_PoI()
one_upper()
