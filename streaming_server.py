from flask import Flask, request, Response, session, redirect, url_for,\
    stream_with_context
import time
import redis

app = Flask(__name__)
red = redis.StrictRedis()

@app.route('/tweets')
def stream():
    # we will use Pub/Sub process to send real-time tweets to client
    def event_stream():
        # instantiate pubsub
        pubsub = red.pubsub()
        # subscribe to tweet_stream channel
        pubsub.subscribe('tweet_stream')
        # initiate server-sent events on messages pushed to channel
        for message in pubsub.listen():
            yield 'data: %s\n\n' % message['data']
            # time.sleep(.1)  # an artificial delay
    return Response(stream_with_context(event_stream()),
                    mimetype="text/event-stream")


if __name__ == '__main__':
    app.run()
