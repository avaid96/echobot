import os
import time
from slackclient import SlackClient
import re
import requests
from fuzzywuzzy import fuzz
import database as db
import pickle

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
SAVE_COMMAND = "save"
GET_COMMAND = "get"

# to be replaced by database add row function
def save(ch, command):
    command = command[len(SAVE_COMMAND):]
    # db call to save the string here
    db.addToDB(ch, msg = command)
    db.save("/volume/slackdb.pickle")
    return True

# to be used to look up a person
def person(name):
    if "name=" in name:
        return True
    return False

# to be used to get history
def get(ch, command):
    command = command[len(SAVE_COMMAND):]
    datereg = re.compile(r'(1[0-2]|[1-9])\/(3[01]|[12][0-9]|[0-9])\/\d{4}')
    date = datereg.search(command)
    querywords = command.split(' ')
    if date is not None:
        date = date.group()
        date.lstrip("0")
        querywords = command.split(' ')
        people = filter((lambda word: person(word)), querywords)
        if len(people) > 0:
            people = map((lambda name: name[5:]), people)
            # here is where you should get a specific person's/people's standup
            # get the object list for this date and iterate through it parsing snippets up for people
            return "here's what happened on " + date + ": \n" + '\n'.join(people)
        # here is where you get the full snippets for that date
        hist = db.get(ch, date)
        return hist
    else:
        return -1

# used to parse a snippet's text to return personwise standup
def parsesnippet(fileid, personlist):
    url = "https://slack.com/api/files.info?token=%s&file=%s&pretty=1" % (SLACK_TOKEN, fileid)
    response = requests.request("GET", url)
    resjson = response.json()
    contentlist = []
    if resjson and "file" in resjson and "url_private_download" in resjson["file"]:
        url = resjson['file']["url_private_download"]
        auth = "Bearer %s" % SLACK_TOKEN
        headers = {
                'authorization': auth,
                    'cache-control': "no-cache",
                        }
        response = requests.request("GET", url, headers=headers)
        sniptxt = response.text
        lines = sniptxt.split("\n")
        for line in lines[1:]:
            if line=="\r":
                continue
            personreg = re.compile(r'([A-Z]|[a-z])+:.+')
            personst = personreg.search(line)
            if personst is not None:
                personst = personst.group()
                splitst = personst.split(":", 1)
                person = split[0]
                if person in personlist:
                    content = split[1]
                    contentlist.append(content)
    if contentlist==[]:
        return None
    return contentlist

# returns true if it is a standup or a sync
def isstandup(sniptxt):
    lines = sniptxt.split("\n")
    matchst = fuzz.partial_ratio("standup", lines[0].lower()) 
    matchsy = fuzz.partial_ratio("sync", lines[0].lower()) 
    if matchst > 70 or matchsy > 70:
        return True
    return False

# to be used to save a snippet where we save the id of it if it meets a criterion
def savesnippet(ch, fileid):
    url = "https://slack.com/api/files.info?token=%s&file=%s&pretty=1" % (SLACK_TOKEN, fileid)
    response = requests.request("GET", url)
    resjson = response.json()
    if resjson and "file" in resjson and "url_private_download" in resjson["file"]:
        url = resjson['file']["url_private_download"]
        if url.endswith(".txt"):
            auth = "Bearer %s" % SLACK_TOKEN
            headers = {
                    'authorization': auth,
                        'cache-control': "no-cache",
                            }
            response = requests.request("GET", url, headers=headers)
            sniptxt = response.text
            if isstandup(sniptxt):
                # put in a database call to save the fileid here
                db.addToDB(ch, msg = fileid)
                db.save("/volume/slackdb.pickle")
                return True
    return False

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + SAVE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(SAVE_COMMAND):
        response = save(channel, command)
        if response == True:
            return
    if command.startswith(GET_COMMAND):
        response = get(channel, command)
        if response == []:
            slack_client.api_call("chat.postMessage", channel=channel,
                          text="No history stored for this date for your channel", as_user=True)
            return
        if response == -1:
            slack_client.api_call("chat.postMessage", channel=channel,
                          text="Please specify a date in (M)M/DD/YYYY format and use --name=\"user\" flags for specific persons", as_user=True)
            return
        for resp in response:
            if "msg" in resp:
                resp = resp["msg"]
            elif "fid" in resp:
                resp = resp["fid"]
            else:
                resp=None
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=resp, as_user=True)
        return
    if command.startswith("id:"):
        # make sure it's a snippet and not another file that we may end up caching
        command = command[3:]
        response = savesnippet(channel, command)  
        if response is False:
            return
        else: 
            response = "I have tracked your file, you can call me if you need it"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and "uploaded" in output['text']:
                if output and 'file' in output and output['file'] and 'id' in output['file']:
                        id = "id:"+output['file']['id']
                        return id, \
                                output['channel']
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if os.path.exists("/volume/slackdb.pickle"):
    db.store = db.load("/volume/slackdb.pickle")
else:
    pickle.dump({}, open("/volume/slackdb.pickle", 'w+'))
    db.store = db.load("/volume/slackdb.pickle")

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
