# -*-coding:Latin-1 -*
"""System, shouldn't be changed for simulations"""



#modules
from queue import PriorityQueue
from functools import total_ordering
import time


#the simulation object (center of everything)
class Simulation():
    """Simulation class: gather all information for a simulation and the event queue
    
    Need a network and a timer, see shape.py
    can set an optional action to execute before each event is computed
    
    Is a callable for the execution of the simulation
    Is iterable to go throught all agents"""
    def __init__(self,network,timer,actions=None):
        """Need a network and a timer"""
        self.q=PriorityQueue()
        self.network=network
        self.timer=timer
        self.actions=actions
        self.agents=[]
    def __call__(self):
        """First compute all agents inside itself
        then run all events stored (still inside itself)
        an optional function can be applied on events before they are computed"""
        self.id_sim=get_id()
        self.execution_time=time.time()
        for a in self.agents:
            a.compute(self)
        while not self.q.empty():
            e=self.q.get()
            if self.actions is not None:
                for action in self.actions:
                    action(e)
            e.run(self)
        self.execution_time=time.time()-self.execution_time
    def put(self,ev):
        """put a new event in the simulation queue"""
        self.q.put(ev)
        self.timer.one_more_time(ev.time)
    def add(self,l):
        """add a new agent in the simulation"""
        self.agents.append(l)
    def set_action(self,*act):
        """define a new (optional) list of actions to do when execute events, such as print"""
        self.actions=act
    def __iter__(self):
        return self.agents.__iter__()
    






#metaclass for the events
class MetaEvent(type):
    """Metaclass for events"""
    def __new__(metacls,nom,base,dico):
        return type.__new__(metacls,nom,base,dico)
    
    def __init__(cls,nom,base,dico):#test the required function are present, instantiate, wrap other methods
        if nom is not "Event" and "run" not in dico:
            raise NotImplementedError("You have to implement a method run(self,simulation) for the event class "+nom)
        type.__init__(cls,nom,base,dico)#instantiate
        def wrapper(init):#do the initiation (of object) test if time is here, put it in simulation
            def output(self,*args1,**args2):
                init(self,*args1,**args2)
                if 'time' not in self.__dict__:
                    raise NotImplementedError("You need a time for the event class "+nom)
            return output
        cls.__init__=wrapper(cls.__init__)
    
@total_ordering
class Event(metaclass=MetaEvent):
    """Event classes need a method run(self,simulation) that puts all other outputs events in the simulation
    Events objects need a time at initialization"""
    def __lt__(self,other):
        return self.time < other.time
    def __eq__(self,other):
        return self.time == other.time
    def __str__(self):
        return "Event at time {} of type {}".format(
                self.time, type(self).__name__)   



 

 #meta class for agents
class MetaAgent(type):
    """Metaclass for agents: to store the list of possible kind"""
    def __new__(metacls,nom,base,dico):
        if "__init__" in dico:
            def wrapper(func):
                def output(self,*args1,**args2):
                    func(self,*args1,**args2)
                    self.put_id()
                return output
            dico["__init__"]=wrapper(dico["__init__"])
        return type.__new__(metacls,nom,base,dico)
            
    def __init__(cls,nom,base,dico):
        if nom != "Agent" and "compute" not in dico:
            raise NotImplementedError("You have to implement a method compute(self,simulation) for the agent class "+nom)
        type.__init__(cls,nom,base,dico)#normal creation
        


class Agent(metaclass=MetaAgent):
    """Class for agents in the simulation
        
        Agent classes :
        -need a function compute(self,simulation)
        
        -can have a constructor
                or
        -can use the Agent constructor: just fill the class attributes "attributes" and "options" 
        
        Agent objects:
        CREATION : type Agent_type.attributes and Agent_type.options to see required fields
        can add an action in the story by a simple call AGENT_NAME(time,action,**kwargs)
        automatically has a unique id_number
        """
    options={}
    attributes=[]
    total_count=1
    def __init__(self,**kwargs):
        self.story=Story()
        self.__dict__.update(type(self).options)
        self.__dict__.update(kwargs)
        for name in type(self).attributes:
            if name not in self.__dict__:
                raise NotImplementedError("You need "+name+" for the agent class "+type(self).__name__)
    def __call__(self,*args,**kwargs):
        self.story.add(*args,**kwargs)
    def set_info(self,**kwargs):
        self.story.set_attribute(**kwargs)
    def put_id(self):
        self.id_number=Agent.total_count
        Agent.total_count+=1
    def __str__(self):
        return "Agent {} of type {}.\n{}".format(self.id_number,type(self).__name__,self.story.__str__())






class Story:
    """story of the movement of an agent, middle between dict and list
    actions are stored in a reverse order in a matter of access: first action that have a time smaller than t is the action executed during t
    
    Is an iterable objects that send back (beginingTime,(actionName,**options)) for all actions
    Can get the action executed at time t with story_name[t]
    
    Reverse_iter can be used to explore actions in the normal order
    It is used for the __str__ function
    
    """
    def __init__(self):
        self.times=[]
        self.actions=[]
    def add(self,t,name,**info):
        self.times.insert(0,t)
        self.actions.insert(0,(name,info))
    def __iter__(self):
        for (pos,t) in enumerate(self.times):
            yield t,self.actions[pos]  
    def __getitem__(self,i):
        for t,act in self:
            if t<=i:
                return t,act
        return None,(None,)
    def reverse_iter(self):
        pos=len(self.times)
        while pos>0:
            pos-=1
            yield self.times[pos],self.actions[pos]
    def __str__(self):
        out=str()
        for t,act in self.reverse_iter():
            out+="begin at {} to {} ".format(t,act)
            out+='\n'
        return out
    def set_attribute(self,**kwargs):
        """Is used for all new attributes to save
        This function can be changed if we don't want informations to be store for a matter of memory. So we don't need to change the processes"""
        self.__dict__.update(**kwargs)
    def get_attribute(self,*args):
        """Is used to get the stored attributes (can be a list)
        return "" if the attribute doesn not exist"""
        return [self.__dict__.get(key,"") for key in args]
    
    
            
def get_id():
    """id of the simulation
    based on the second it is launched"""
    return "{0}{7:03}{3:02}{4:02}{5:02}".format(*time.localtime())




