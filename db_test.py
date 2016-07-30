import database
import os 

def testDB():
	# new store
	database.store = {}
	# add to database
	database.addToDB("sec", fid = "test")
	database.addToDB("sec", msg = "anotherone")
	# get from database
	assert len(database.get("sec", database.getDate())) == 2
	assert (database.get("sec", database.getDate()))[0]['fid'] == "test"
	assert (database.get("sec", database.getDate()))[1]['msg'] == "anotherone"
	assert (database.get("oth", database.getDate())) == []
	# save database to pickle
	database.save("temp.pickle")
	# remove from database
	database.remove(database.getDate())
	assert database.get("sec", database.getDate()) == []
	# load database from pickle
	database.store = database.load("temp.pickle")
	# get from database
	assert (database.get("sec", database.getDate()))[0]['fid'] == "test"
	assert (database.get("sec", database.getDate()))[1]['msg'] == "anotherone"
	os.remove("temp.pickle")

if __name__ == "__main__":
	testDB()
