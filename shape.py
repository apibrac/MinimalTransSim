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
    

    
    
    ### NOT SURE IT IS USEFUL !!!!

#TYPICAL DEMAND GENERATOR AND FUNCTION ON IT
def demand_generator(*args):#numberOfDriver,agentType):
    """simulation (for the network and the timer), *args is list of tuple with (numberOfAgent,AgentType,kwargsFunction,kwargs)
    kwargs and kwargsFunction are dico with paramters for agent creation. kwargs will just be thrown, kwargsFunction are callable that will be called"""
    out=[]
    for agent in args:
        number=agent[0]
        agentType=agent[1]
        optionsF={}
        if len(agent) > 2:
            optionsF=agent[2]
        options2={}
        if len(agent) > 3:
            options2=agent[3]
        for i in range(number):
            options=dict(options2)
            for name,opt in optionsF.items():
                options[name]=opt()
            a=agentType(**options)
            out.append(a)
            #a.compute(simulation)
    return out


def observation(agents,function,type=None,filtering_function=None,**options2):
    """create a function of *options1 arguments from a list of agents and a function defined and applied on 
    (agent,*options1,**options2). The list of agents can be filtered by a type or a filtering_function giving a boolean answer"""
    def functionOut(*options1):
        out=[]
        for agent in agents:
            if (type is None or isinstance(agent, type)) and (filtering_function is None or filtering_function(agent)):
                out.append(function(agent,*options1,**options2))
        return out
    return functionOut




