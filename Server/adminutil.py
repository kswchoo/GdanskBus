#!/usr/bin/env python
# -*- coding: utf8 -*-

import argparse
import sys
from GdanskBusServer.models import Route
from GdanskBusServer.database import init_db, db_session
from GdanskBusServer.crawler import updateRoutes, updateRouteDetail
from GdanskBusServer.metadata import setMetadata
from time import time

parser = argparse.ArgumentParser(description='GdanskBus data admin tool')
parser.add_argument('action', choices=["init-db", "update-routes", "update-route-details"])
parser.add_argument('--route')
args = parser.parse_args()

def updateTimestamp():
    print "Timestamp updated"
    setMetadata("dataTimestamp", int(time()))

if args.action == "init-db":
    print "Database created!"
    init_db()
elif args.action == "update-routes":
    print "Downloading routes"
    updateRoutes("http://www.ztm.gda.pl/rozklady/")
    updateTimestamp()
elif args.action == "update-route-details":
    if args.route is not None:
        route = db_session.query(Route).get(args.route)
        if route is not None:
            print "*** Downloading route %s ***" % route
            updateRouteDetail(route)
            updateTimestamp()
        else:
            print "Route not exists."
    else:
        routes = db_session.query(Route).all()
        for route in routes:
            print "*** Downloading route %s ***" % route
            for reyty in range(3):
                try:
                    updateRouteDetail(route)
                    break
                except:
                    print "Error orccured. %s" % sys.exc_info()[0]
            updateTimestamp()
