#!/usr/bin/python
# -*- coding: utf8 -*-

from database import db_session
from models import Metadata

def getMetadata(key):
    metadata = db_session.query(Metadata).get(key)
    if metadata is None:
        print "None"
        return None
    else:
        return metadata.value

def setMetadata(key, value):
    updated = Metadata(key, value)
    db_session.merge(updated)
    db_session.commit()
