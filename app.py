#!/usr/bin/env python

import os
from flask import Flask, render_template, jsonify
import requests
import xmltodict
from icalendar.cal import Calendar
from birdy.twitter import UserClient

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/bart")
def bart():
    return jsonify(xmltodict.parse(requests.get('http://api.bart.gov/api/etd.aspx?cmd=etd&orig=16th&key=MW9S-E7SL-26DU-VV8V').text))

@app.route("/events")
def events():
    cal = Calendar.from_ical(requests.get('http://ratchet.noisebridge.systems/~phong/events.ical').text)
    events = []
    for event in cal.walk('vevent'):
        events.append({
            'start': event.decoded('dtstart'),
            'title': event.decoded('summary')
        })
    return jsonify(events=events)

lastTweet = 0

@app.route("/twitter")
def twitter():
    response = client.api.search.tweets.get(q='noisebridge')
    return jsonify(tweets=response.data)

if __name__ == "__main__":
    app.run(debug=True)
