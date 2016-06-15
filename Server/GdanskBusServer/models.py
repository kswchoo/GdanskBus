from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Metadata(Base):
    __tablename__ = 'metadatas'
    key = Column(String(32), primary_key=True)
    value = Column(String(255), nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

class Route(Base):
    __tablename__ = 'routes'
    id = Column(String(5), primary_key=True)
    type = Column(Integer, nullable=False)
    link = Column(String(255), nullable=True)
    directions = relationship("RouteDirection")

    def __init__(self, id, type, link):
        self.id = id
        self.type = type
        self.link = link

    def __repr__(self):
        return '<Route %s Type %d>' % (self.id, self.type)

class RouteDirection(Base):
    __tablename__ = 'directions'
    id = Column(Integer, primary_key=True)
    routeid = Column(String(5), ForeignKey('routes.id'))
    terminal = Column(String(255), nullable=False)
    route = relationship("Route", back_populates="directions")

    def __init__(self, routeid, terminal):
        self.routeid = routeid
        self.terminal = terminal

    def __repr__(self):
        return '<RouteDirection %d %s %s>' % (self.id, self.routeid, self.terminal)

class RouteDirectionStop(Base):
    __tablename__ = 'direction_stops'
    id = Column(Integer, primary_key=True)
    directionid = Column(Integer, ForeignKey('directions.id'))
    stopid = Column(Integer, ForeignKey('stops.id'))
    seq = Column(Integer, nullable=False)

    def __init__(self, directionid, stopid, seq):
        self.directionid = directionid
        self.stopid = stopid
        self.seq = seq

    def __repr__(self):
        return '<RouteDirectionStop %s %s %s>' % (self.directionid, self.stopid)

class Stop(Base):
    __tablename__ = 'stops'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    lat = Column(Float, nullable=True)
    long = Column(Float, nullable=True)

    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

    def __repr__(self):
        return '<Stop %s>' % (self.id)
