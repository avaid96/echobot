docker build -t standup .

You'll need an env.list file containing your:
1. SLACK_BOT_TOKEN
2. BOT_ID
3. SLACK_TOKEN

docker run -v $PWD/volume/:/volume/ --env-file ./env.list -it --rm --name standupbot standup

The program will create a database file in $PWD/volum/slackdb.pickle and cache things that you save in that file by date. The .gitignore is set up not to track this file
