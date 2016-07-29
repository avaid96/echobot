from pymongo import MongoClient

# use mongoclient to create a connection
client = MongoClient()
db = client.primer

def addToDB(date, person, data):
# Add in datetime
	result = db.standup.insert_one (
		{
			"date": date,
			"speaker": person,
			"data":data
		}
	)
	return result.inserted_id

# Either pass in one field or many fields (dictionary)
def findField(d):
	docs = []
	cursor = db.standup.find(d)
	for document in cursor:
		docs.append(document)
	return docs



# Add tag

def removeValue(d):
	count = db.standup.count({field:value})
	print "Deleting "  + str(count) + " entries"
	cursor = db.standup.delete_many(d)

