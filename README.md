docker build -t standup .

You'll need an env.list file containing your:
1. SLACK_BOT_TOKEN
2. BOT_ID
3. SLACK_TOKEN

docker run --env-file ./env.list -it --rm --name standupbot standup
