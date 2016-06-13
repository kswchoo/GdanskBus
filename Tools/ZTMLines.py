#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from collections import namedtuple
from bs4 import BeautifulSoup
import json
import csv
import os.path

baseurl = "http://www.ztm.gda.pl/rozklady/"

Route = namedtuple("Route", ["name", "link"])
RouteDetail = namedtuple("RouteDetail", ["name", "type", "directions"])
RouteDirection = namedtuple("RouteDirection", ["terminal", "stops"])
Stop = namedtuple("Stop", ["name", "code"])
Location = namedtuple("Location", ["lat", "long", "annotation"])

def getRoutes(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all("tr")
    routes = []
    for tr in table:
        td = tr.find("td")
        if td is not None:
            a = td.find("a")
            name = a.text.encode('ascii','ignore')
            if not name.startswith("F"):
                route = Route(name, baseurl + a["href"])
                routes.append(route)
                print "  --> Route %s %s" % (route.name, route.link)
    return routes

def getRouteDetail(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    routeDiv = soup.find("div", class_="route-number")
    routeType = {
        "Tramwaje": 1,
        "Autobusy": 2,
        "Nocne autobusy": 4,
        "Tramwaj wodny": 8,
    }.get(routeDiv.find("img")["title"], 0)
    routeName = routeDiv.find("a").text

    directions = []
    for table in soup.find_all("table", class_="route"):
        trs = table.find_all("tr")
        headTd = trs[0].find("td")
        if headTd is not None:
            terminal = headTd.find("b").text
            print "  --> Terminal %s" % terminal
            stops = []
            for tr in trs[2:-1]:
                stopA = tr.find("a")
                if stopA is not None:
                    stopLink = baseurl + stopA["href"]
                    stop = getStopDetails(stopLink)
                    stops.append(stop)
                    print "       --> Stop %s %s %s" % (stop.name, stop.code, stopLink)
            directions.append(RouteDirection(terminal, stops))
    return RouteDetail(routeName, routeType, directions)

def getStopDetails(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    stopDiv = soup.find("div", class_="current-stop")
    name = stopDiv.find("a").text
    code = int(stopDiv.find("span").text)
    return Stop(name, code)

routes = []
stops = {}
stopTypes = {}
outRoutes = []


print "Downloading route list ..."
routeMetas = getRoutes(baseurl)

for routeMeta in routeMetas:
    print "Downloading route details for route %s ..." % routeMeta.name
    route = getRouteDetail(routeMeta.link)
    routes.append(route)
    for direction in route.directions:
        for stop in direction.stops:
            stops[stop.code] = stop

print "Organizing routes ..."
for route in routes:
    directions = []
    for direction in route.directions:
        directionStops = []
        for directionStop in direction.stops:
            directionStops.append(directionStop.code)
            if directionStop.code in stopTypes:
                stopTypes[directionStop.code] = stopTypes[directionStop.code] | route.type
            else:
                stopTypes[directionStop.code] = route.type
        directions.append({"terminal:": direction.terminal, "stops": directionStops})
    outRoutes.append({"name": route.name, "type": route.type, "directions": directions})

print "Loading stops.csv ..."
stopLocations = {}
if os.path.isfile("stops.csv"):
    with open('stops.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
        for row in reader:
            stopLocations[int(row[0])] = Location(float(row[1]), float(row[2]), row[3])

print "Organizing stops ..."
outStops = []
for stop in stops.values():
    item = {"code": stop.code, "name": stop.name, "type": stopTypes[stop.code]}
    if stop.code in stopLocations.keys():
        item["lat"] = stopLocations[stop.code].lat
        item["long"] = stopLocations[stop.code].long
    outStops.append(item)

print "Writing meta.json ..."
with open("meta.json", "w") as jsonfile:
    json.dump({"routes": outRoutes, "stops": outStops}, jsonfile)