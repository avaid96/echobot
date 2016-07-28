from pymongo import MongoClient

# use mongoclient to create a connection
client = MongoClient()
db = client.primer

def addToDB(date, person, data):
	result = db.standup.insert_one(
		{
			"date": date,
			"speaker": person,
			"data":data
		}
	)
	return result.inserted_id

def findField(field, value):
	cursor = db.standup.find({field: value})
	for document in cursor:
		print (document)

	return cursor.toArray()

