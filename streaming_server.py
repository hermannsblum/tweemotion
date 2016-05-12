from flask import Flask, request, Response, session
import time

app = Flask(__name__)


def event_stream():
    yield 'data: hi'
    time.sleep(.1)  # an artificial delay


@app.route('/post', methods=['POST'])
def post():
    message = request.form['message']
    user = session.get('user', 'anonymous')


@app.route('/stream')
def stream():
    if request.headers.get('accept') == 'text/event-stream':
        return Response(event_stream(),
                        mimetype="text/event-stream")


if __name__ == '__main__':
    app.run()
