import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import requests
import json


# --------------------------------------------
# to get enviornment variables from .env files
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# /--------------------------------------------

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])  # slack webclient
BOT_ID = client.api_call("auth.test")['user_id']  # return ID of BOT

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)  # for handling events


# --------------------------------------------
#to handel events
@app.route("/slack/events")
def slack_event_tester():
    client.chat_postMessage(channel='test', text='i got the event ')


# --------------------------------------------

#Fetching Title and URL from our API

response_API = requests.get('https://pjmeme.ml/meme')
data = response_API.text
parse_json = json.loads(data)
title = parse_json['title']
post_preview = parse_json['url']


# --------------------------------------------
#function to fetch API
def fnc1():
    global response_API, data, parse_json, title, post_preview
    response_API = requests.get('https://pjmeme.ml/meme')
    data = response_API.text
    parse_json = json.loads(data)
    title = parse_json['title']
    post_preview = parse_json['url']


# --------------------------------------------

# --------------------------------------------
#everytime /meme enddpoint occurs this will run
@app.route('/meme', methods=["GET", "POST"])
def meme():
    fnc1()#fetch api when /meme is called
    client.chat_postMessage(channel="test", attachments=[{
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{title}",
                    "emoji": True
                }
            },
            {
                "type": "image",
                "image_url": f"{post_preview}",
                "alt_text": "meme"
            }
        ]
    }]) #post message to channel 
    return Response(), 200


# --------------------------------------------


if __name__ == '__main__':
    app.run(debug=True) #run the Flask app
