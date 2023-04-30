import logging
import logging.config
import os
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

import logic.responses as responses

CONFIG_DIR = "./config"
LOG_DIR = "./logs"

# find .env file in parent directory
env_file = find_dotenv()
load_dotenv()


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
logger = logging.getLogger(__name__)


@app.route("/")
def hello():
    return "Hello from Optimus Prime!"


@app.route("/api/request", methods=['POST'])
def slack_request():
    incoming_request = request.get_json()
    logger.info("Request received")
    logger.debug(f'incoming json request = {incoming_request}')
    if incoming_request.get("type") is not None and 'url_verification' == incoming_request.get("type"):
        logger.info(f"Responding to challenge ")
        challenge, http_code = responses.respond_to_challenge(incoming_request)
        logger.info(f"Responding with http code {http_code}")
        return {
            'statusCode': http_code,
            'Content - type': 'text/plain',
            'body': challenge
        }


if __name__ == "__main__":
    setup_logging()
    app.run(host='0.0.0.0', port=3000, debug=True)
    logger.info("Starting app")