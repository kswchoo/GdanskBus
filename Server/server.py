#!/usr/bin/env python
# -*- coding: utf8 -*-

from flask import Flask,redirect,jsonify
from GdanskBusServer.database import db_session
from GdanskBusServer.metadata import getMetadata
from flask_ask import Ask, statement
import requests
from bs4 import BeautifulSoup
import string
import re

app = Flask(__name__)
ask = Ask(app, '/ask-endpoint')

@app.route('/')
def hello_world():
    return redirect("https://itunes.apple.com/app/id1123553048", code=302)

@app.route('/data/version')
def version():
    return jsonify({"apiVersion": 2, "dataTimestamp": int(getMetadata("dataTimestamp"))})

@app.route('/stops')
def getStops():
	infile = open('stops.json', 'r')  # Open the file for reading.
	data = infile.read()  # Read the contents of the file.
	infile.close()  # Close the file since we're done using it.
	return data

@app.route('/stop/<stop>')
def getStop( stop ):
	stop = int(stop)
	print('----STOP %d----' % stop)
	page = requests.get('http://www.ztm.gda.pl/rozklady/pobierz_SIP.php?n[0]=%d' % stop)
	soup = BeautifulSoup(page.content, 'html.parser')
	items = soup.contents[1].split('<br>')[-1].split('\n')
	items = map(string.strip, items)
	items = [ x for x in items if x.startswith('[') ]
	response = []
	for item in items:
		row = {}
		components = item.split('=>')
		row['seq'] = int(re.sub('[^0-9]', '', components[0]))
		values = components[1].split(';')
		arrives = string.strip(values[0])
		if ':' in arrives:
			row['arrivesAt'] = arrives
		else:
			row['arrivesIn'] = int(arrives)
		row['stopCode'] = int(values[1])
		row['stopName'] = values[2]
		row['direction'] = values[3]
		row['line'] = values[4]
		row['extra1'] = values[5]
		if not values[6]: row['car'] = values[6]
		row['extra2'] = values[7]
		response.append(row)
	return jsonify(response)

@ask.intent('ArrivalsForStopId')
def arrivalsForStopId(stopId):
    stop = int(stopId)
    print('----STOP %d----' % stop)
    page = requests.get('http://www.ztm.gda.pl/rozklady/pobierz_SIP.php?n[0]=%d' % stop)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.contents[1].split('<br>')[-1].split('\n')
    items = map(string.strip, items)
    items = [x for x in items if x.startswith('[')]
    response = ""
    for item in items:
        components = item.split('=>')
        seq = int(re.sub('[^0-9]', '', components[0]))
        values = components[1].split(';')
        arrives = string.strip(values[0])
        line = values[4]
        if ':' in arrives:
            response += "Line number %s will arrives at %s. " % (line, arrives)
        elif arrives == '0':
            response += "Line number %s will arrive now. " % line
        else:
            response += "Line number %s will arrives in %s minutes. " % (line, arrives)
        if seq > 4:
            break
    if len(response) == 0:
        response = "<speak>There are no arrival information for now.</speak>"
    else:
        response = "<speak>Here's arrival information for stop <say-as interpret-as='cardinal'>%s</say-as>. %s</speak>" % (stop, response)
    return statement(response)

@ask.intent('ArrivalsForStopName')
def arrivalsForStopName(stopName, boundsForName):
    stop = 0
    print "StopName %s" % stopName
    if stopName == "tetramayera" and (boundsForName == "zesichie" or boundsForName == "hodovitskiego"):
        stop = 2040
    if stopName == "hodovitskiego" and (boundsForName == "oliva" or boundsForName == "hodovitskiego" or boundsForName == "tetramayera"):
        stop = 2007
    print('----STOP %d----' % stop)
    page = requests.get('http://www.ztm.gda.pl/rozklady/pobierz_SIP.php?n[0]=%d' % stop)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.contents[1].split('<br>')[-1].split('\n')
    items = map(string.strip, items)
    items = [x for x in items if x.startswith('[')]
    response = ""
    for item in items:
        components = item.split('=>')
        seq = int(re.sub('[^0-9]', '', components[0]))
        values = components[1].split(';')
        arrives = string.strip(values[0])
        line = values[4]
        if ':' in arrives:
            response += "Line number %s will arrives at %s. " % (line, arrives)
        elif arrives == '0':
            response += "Line number %s will arrive now. " % line
        else:
            response += "Line number %s will arrives in %s minutes. " % (line, arrives)
        if seq > 4:
            break
    if len(response) == 0:
        response = "<speak>There are no arrival information for now.</speak>"
    else:
        response = "<speak>Here's arrival information for stop <say-as interpret-as='cardinal'>%s</say-as>. %s</speak>" % (stop, response)
    return statement(response)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
