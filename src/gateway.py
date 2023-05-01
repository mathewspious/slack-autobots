import logging
import logging.config
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from loguru import logger
import sys

import logic.responses as responses

CONFIG_DIR = "./config"
LOG_DIR = "./logs"

# find .env file in parent directory
env_file = find_dotenv()
load_dotenv()

client = WebClient(token=os.environ.get('slack_token'))
print(f"client = {client.token}")


def setup_logging():
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.ini")
    config_path = "/".join([CONFIG_DIR, config])
    timestamp = datetime.now().strftime("slack-autobots-%Y%m%d-%H:%M:%S")
    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{LOG_DIR}/{timestamp}.log"},
    )


app = Flask(__name__)

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level: <8}</level> <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

@app.route("/")
def hello():
    return "Hello from Optimus Prime!"


@app.route("/api/request", methods=['POST'])
def slack_request():
    incoming_request = request.get_json()
    logger.info("Request received")
    print(f"Request received {incoming_request}")

    logger.info("request type {}", incoming_request.get("event"))

    if incoming_request.get("event") is not None and incoming_request.get("event").get("type") is not None and "message" == incoming_request.get("event").get("type"):
        logger.info(f"Responding to message ")
        print(f"Responding to message {incoming_request}")
        response_txt, channel_id = responses.respond_to_message(incoming_request)
        result = client.chat_postMessage(
            channel=channel_id,
            text=response_txt
        )
        logger.info("chat response status = {}", result)
    elif incoming_request.get("type") is not None and 'url_verification' == incoming_request.get("type"):
        logger.info(f"Responding to challenge ")
        print(f"Responding to challenge ")
        challenge, http_code = responses.respond_to_challenge(incoming_request)
        logger.info(f"Responding with http code {http_code}")
        return {
            'statusCode': http_code,
            'Content - type': 'text/plain',
            'body': challenge
        }


if __name__ == "__main__":
    #setup_logging()
    app.run(host='0.0.0.0', port=3000, debug=True)
    logger.info("Starting app")
