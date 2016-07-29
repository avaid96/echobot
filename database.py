import time
import datetime

store = {}

# dictionary format: data=[{fid: val1}, {fid: val2}, {msg: val3}]
def addToDB(**kwargs):
	date = getDate()

	if 'msg' in kwargs:
		input_type = 'msg'
		d = kwargs['msg']
	if 'fid' in kwargs:
		input_type = 'fid'
		d = kwargs['fid']

        entry = {input_type: d}

	if date in store:
		ls = store[date].append(entry)
		store[date] = ls
	else:
		store[date] = [entry]
	return entry

# get either entries with specified date or date and other flags 
def get(date):
	data = store[date]
	return data

def getDate():
	now = datetime.datetime.now()
	date = now.year + now.month + now.day
	return date

def remove(date):
	if date in store:
	store.pop(date, None)
