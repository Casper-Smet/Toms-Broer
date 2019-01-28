import mysql.connector



def connect_database():
	database = mysql.connector.connect(
		# host='145.89.166.209',
		host='localhost',
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
	update = 'update points_of_interest set searched = searched + 1 where ID =' + str(poi_id)
	
	database = connect_database()
	cursor = database.cursor()
	
	cursor.execute('use tomsbroer;')
	cursor.execute(update)
	database.commit()

# get_PoI()
one_upper()
