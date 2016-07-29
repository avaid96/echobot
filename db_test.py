import database
import os 

def testDB():
	# new store
	database.store = {}
	# add to database
	database.addToDB(fid = "test")
	database.addToDB(msg = "anotherone")
	# get from database
	assert (database.get(database.getDate()))[0]['fid'] == "test"
	assert (database.get(database.getDate()))[1]['msg'] == "anotherone"
	# save database to pickle
	database.save("temp.pickle")
	# remove from database
	database.remove(database.getDate())
	assert database.get(database.getDate()) == -1
	# load database from pickle
	database.store = database.load("temp.pickle")
	# get from database
	assert (database.get(database.getDate()))[0]['fid'] == "test"
	assert (database.get(database.getDate()))[1]['msg'] == "anotherone"
	os.remove("temp.pickle")

if __name__ == "__main__":
	testDB()
