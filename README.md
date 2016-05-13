# tweemotion
twitter sentiment visualization

# how to tun this

1. start a redis-server for message passing

2. start the twitter stream with python twitter_stream.py publish
(this will process the tweets and publish processed data to redis)

3. start the local web server with python streaming_server.py
(this will publish our js files and also create an endpoint that streams processed tweets to the js application)

4. you will find the application at localhost:5000/static/hermann.html (which we can change later, it was my working file ;) )
