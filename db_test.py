import database

def main():
	objID = database.addToDB("June", "Jess", "Merged first PR")
	objID = database.addToDB("June", "Jess", "Merged first PR")
	field = {"date":"June"}
	array = database.findField(field)
	for row in array:
		print row 

	fields = {"date":"June", "speaker":"Jess"}
	array = database.findField(fields)
	for row in array:
		print row 

main()
