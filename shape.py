# -*-coding:Latin-1 -*
"""Basic generators of simulations elements:
network, timer, demand
Other typical generator can be added later"""



#modules
from random import random
from math import sqrt
import matplotlib.patches as patch




#Basic envelopes
class Network:
    def __init__(self,position_generator,travel_time,travel_distance,gpatch,Xsize=None,Ysize=None):
        self.position_generator=position_generator
        self.travel_time=travel_time
        self.get_patch=gpatch
        self.travel_distance=travel_distance
        self.Xsize=Xsize
        self.Ysize=Ysize
        
        
class Timer:
    def __init__(self,last_departure):
        self.last_departure=last_departure
        self.finish_time=last_departure
    def random_time(self):
        return random()*self.last_departure
    def one_more_time(self,t):
        if t>self.finish_time:
            self.finish_time=t





#PRACTICAL OBJECTS
def rectangle(X,Y,basic_speed):
    """rectangle with x from X[0] to X[1], and same for y"""
    def position():
        x=X[0]+random()*(X[1]-X[0])
        y=Y[0]+random()*(Y[1]-Y[0])
        return (x,y)
    def travel(p1,p2):
        dist=(p1[0]-p2[0])**2+(p1[1]-p2[1])**2
        dist=sqrt(dist)
        return dist/basic_speed
    def dist_travelled(t):
        return t*basic_speed
    def gpatch():
        return patch.Rectangle((X[0],Y[0]),X[1]-X[0], Y[1]-Y[0])
    return Network(position,travel,dist_travelled,gpatch,X,Y)

def square(a,basic_speed):
    """square of size a"""
    return rectangle((0,a),(0,a))
    

def circle(R, basic_speed):
    """circle of radius R"""
    S=(-R,R)
    def position():
        x,y=R,R#begin outside the circle
        while x*x+y*y > R*R:#means outside the circle
            x=S[0]+random()*(S[1]-S[0])
            y=S[0]+random()*(S[1]-S[0])
        return (x,y)
    def travel(p1,p2):
        dist=(p1[0]-p2[0])**2+(p1[1]-p2[1])**2
        dist=sqrt(dist)
        return dist/basic_speed
    def dist_travelled(t):
        return t*basic_speed
    def gpatch():
        return patch.Circle((0,0),R)
    return Network(position,travel,dist_travelled,gpatch,S,S)
    


