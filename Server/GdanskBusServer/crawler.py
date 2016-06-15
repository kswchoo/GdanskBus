#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
from models import Route, RouteDirection, Stop, RouteDirectionStop
from database import db_session

baseurl = "http://www.ztm.gda.pl/rozklady/"

def updateRoutes(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all("tr")
    for tr in table:
        td = tr.find("td")
        if td is not None:
            a = td.find("a")
            id = a.text.encode('ascii','ignore')
            if not id.startswith("F"):
                route = Route(id, 0, baseurl + a["href"])
                existing = db_session.query(Route).get(route.id)
                if existing:
                    route.type = existing.type
                    db_session.query(Route).filter(Route.id == route.id).delete()
                    db_session.add(route)
                    print "Updated metadata - Route %s - %s" % (route.id, route.link)
                else:
                    db_session.add(route)
                    print "Added metadata - %s - %s" % (route.id, route.link)
                db_session.commit()

def updateRouteDetail(route):
    page = requests.get(route.link)
    soup = BeautifulSoup(page.content, "html.parser")

    routeDiv = soup.find("div", class_="route-number")
    route.type = {
        "Tramwaje": 1,
        "Autobusy": 2,
        "Nocne autobusy": 4,
        "Tramwaj wodny": 8,
    }.get(routeDiv.find("img")["title"], 0)
    routeName = routeDiv.find("a").text
    db_session.merge(route)
    db_session.commit()

    print "Type for route %s determined = %d" % (route.id, route.type)

    dirs = db_session.query(RouteDirection).filter(RouteDirection.routeid == route.id).all()
    for direction in dirs:
        db_session.query(RouteDirectionStop).filter(RouteDirectionStop.directionid == direction.id).delete()
        db_session.commit()

    db_session.query(RouteDirection).filter(RouteDirection.routeid == route.id).delete()
    db_session.commit()

    for table in soup.find_all("table", class_="route"):
        trs = table.find_all("tr")
        headTd = trs[0].find("td")
        if headTd is not None:
            terminal = headTd.find("b").text
            print "Terminal %s" % terminal
            newDirection = RouteDirection(route.id, terminal)
            db_session.add(newDirection)
            db_session.commit()

            seq = 0
            for tr in trs[2:-1]:
                stopA = tr.find("a")
                if stopA is not None:
                    stopLink = baseurl + stopA["href"]
                    newStop = getStopDetails(stopLink)
                    oldStop = db_session.query(Stop).get(newStop.id)
                    if oldStop is None:
                        newStop.type = route.type
                    else:
                        newStop.type = oldStop.type | route.type
                    db_session.merge(newStop)
                    db_session.commit()
                    print "--> Stop %s %s %s" % (newStop.name, newStop.id, newStop.type)

                    seq = seq + 1
                    db_session.add(RouteDirectionStop(newDirection.id, newStop.id, seq))
                    db_session.commit()

def getStopDetails(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    stopDiv = soup.find("div", class_="current-stop")
    name = stopDiv.find("a").text.replace(u"(n/ż)","").strip()
    id = int(stopDiv.find("span", title="Numer słupka").text)
    return Stop(id, name, 0)
