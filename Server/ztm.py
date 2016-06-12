#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
import string
import re

from flask import Flask, jsonify
app = Flask(__name__)

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


if __name__ == "__main__":
	app.run(host='0.0.0.0')