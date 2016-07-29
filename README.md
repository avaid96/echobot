docker build -t standup .
docker run --env-file ./env.list -it --rm --name standupbot standup
