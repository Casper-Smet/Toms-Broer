import mysql.connector

database = mysql.connector.connect(
	host='145.89.166.209',
	user='tom',
	password='broer'
)

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

print(data[:3])