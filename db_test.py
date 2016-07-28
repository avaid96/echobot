import database

def main():
	objID = database.addToDB("June", "Jess", "Merged first PR")
	print objID
	array = database.findField("date", "June")
	print array
	for x in array:
		print x
main()
