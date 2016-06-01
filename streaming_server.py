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

    response = Response(stream_with_context(event_stream()),
                        mimetype="text/event-stream")
    response.headers['Expires'] = "Thu, 01 Dec 1983 20:00:00 GMT"
    response.headers['Cache-Control'] = 'no-cache'
    return response



if __name__ == '__main__':
    port = raw_input('set port:')
    #app.run(host='188.166.148.125', port=int(port))
    app.run(host='188.166.148.125', port=int(port))
