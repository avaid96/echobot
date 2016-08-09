# Using this integration, you can

1. Save messages by date by calling @<botname> save message
2. Saves all snippets than contain a >70% partial fuzzy match of the words stand-up or sync in their first line
- To be able to search person-wise later, you should structure standup/sync items in the form:
```
standup
person1: did this
person2: did another thing
```
3. Get all items saved on a particular date by calling @<botname> get (M)M/DD/YYYY
4. Get a particular person, person1's sync item from a date by calling @<botname> get (M)M/DD/YYYY name=person1

# How to use this integration

You'll need an env.list file containing your:
1. SLACK_BOT_TOKEN
2. BOT_ID
3. SLACK_TOKEN

Run: 

docker build -t standup .

docker run -v $PWD/volume/:/volume/ --env-file ./env.list -it --rm --name standupbot standup

The program will create a uses a pickle as a database and will create a database file in $PWD/volume/slackdb.pickle and cache things that you save in that file by date. The .gitignore is set up not to track this file


