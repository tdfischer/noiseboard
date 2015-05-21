#!/usr/bin/env python

from flask import Flask, render_template, jsonify
import requests
import xmltodict

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/bart")
def bart():
  return jsonify(xmltodict.parse(requests.get('http://api.bart.gov/api/etd.aspx?cmd=etd&orig=16th&key=MW9S-E7SL-26DU-VV8V').text))

if __name__ == "__main__":
    app.run(debug=True)
