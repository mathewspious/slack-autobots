import logging
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv, find_dotenv
import os
import ssl
import certifi
from slack_sdk import WebClient
from flask import Flask, request

logging.basicConfig(level=logging.DEBUG)

env_file = find_dotenv()
load_dotenv()

ssl_context = ssl.create_default_context(cafile=certifi.where())
web_client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'), ssl=ssl_context)

app = App(client=web_client)


@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.event("app_mention")
def event_test(body, say, logger):
    logger.info(body)
    say("What's up?")


@app.event("message")
def handle_message():
    pass


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# pip install -r requirements.txt
# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***
# FLASK_APP=app.py FLASK_ENV=development flask run -p 3000
