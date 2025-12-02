import os
from slackeventsapi import SlackEventAdapter
from app import app

slack_events_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'],'/slack/events',app)