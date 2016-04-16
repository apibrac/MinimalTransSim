
from CircleNet.system import Event, Agent

# the algo module (detailed)
class MatchingPlatform:
    """Store all passenger announces
    When a driver look for a passenger, compute and send the list of coherent announces (based on window time)
    When a match is made delete the announce
    
    Proximity is not watched
    
    NEED: "Driver" & "Passenger":
        print(Driver.attributes), print(Passenger.attributes)"""
    def __init__(self,benefits_function,simu):
        self.passengerList={}
        self.benefits=benefits_function
        self.simulation=simu
    def addPassenger(self,agent,lastDeparture,origin,destination):
        """Add a passenger with all needed info"""
        self.passengerList[agent]={"ld":lastDeparture,"O":origin,"D":destination}
    def checkPotentialMatching(self,departureTime,origin):#information of driver
        """send the list of compatible announce (with the departureTime)"""
        out=[]
        for passenger in self.passengerList:
            p_info=self.passengerList[passenger]
            travelTime=self.simulation.network.travel_time(origin,p_info["O"])#travel time from the driver origin to the passenger origin
            if departureTime+travelTime <= p_info["ld"]:#check compatibility
                out.append(self.sendAnnounce(passenger,p_info))
        return out
    def sendAnnounce(self,agent,info):
        """set the information send to a driver when a coherent passenger is found"""
        bene=self.benefits(info["O"],info["D"],self.simulation.network)
        return (agent,{"O":info["O"],"D":info["D"],"b":bene})
    def retreivePassenger(self,agent):
        """delete an announce when accepted or obsolete"""
        if agent in self.passengerList:
            del(self.passengerList[agent])
            return True
        return False
        
        
        
        
        

        
        
#EVENT
class PublishAnnounce(Event):
    """Event when a passenger publish an announce"""
    def __init__(self, agent):
        self.time=agent.publishing_time
        self.agent=agent
    def run(self,simulation):
        agent=self.agent
        simulation.matchingAlgo.addPassenger(agent,agent.last_departure_time,agent.position,agent.destination)
        simulation.put(RetreiveAnnounce(agent,agent.last_departure_time))
        self.agent(self.time,"waiting",position=agent.position)
    def __str__(self):
        return super().__str__() + " by agent " + str(self.agent.id_number)
        
class RetreiveAnnounce(Event):
    """Delete a passenger's announce
        if really delete it means the passenger didn't find a proper driver
        otherwise this event is useless"""
    def __init__(self,agent,time):
        self.time=time
        self.agent=agent
    def run(self,simulation):
        if simulation.matchingAlgo.retreivePassenger(self.agent):
            self.agent(self.time,"missed")
    def __str__(self):
        return super().__str__() + " by agent " + str(self.agent.id_number)
        
        
class WatchAnnounce(Event):
    """A driver ask for potential passengers"""
    def __init__(self,agent,watching_time):
        self.time=watching_time
        self.agent=agent
    def __str__(self):
        return super().__str__() + " by agent " + str(self.agent.id_number)
    def run(self,simulation):
        #compute at what time the driver can leave:
        possible_departure=max(self.agent.departure_window[0],self.time)
        #look all potential matchings
        potentialMatching=simulation.matchingAlgo.checkPotentialMatching(possible_departure,self.agent.position)
        agentMatched=None
        bestRate=0
        for match in potentialMatching:
            rate=self.agent.rating(**match[1],n=simulation.network,t=possible_departure)
            if rate > bestRate:#driver accept the match
                agentMatched=match[0]
        if agentMatched:#we have a match!
            simulation.matchingAlgo.retreivePassenger(agentMatched)
            self.agent(self.time,"matched",passenger=agentMatched.id_number)
            agentMatched(self.time,"matched",driver=self.agent.id_number)
            l_points=[("Od",self.agent.position),("Op",agentMatched.position),("Dp",agentMatched.destination),("Dd",self.agent.destination)]
            l_agents=[[self.agent,"Od","Dd"],[agentMatched,"Op","Dp"]]
            t=Travel(possible_departure,l_points,l_agents)
            simulation.put(t)
        else:
            next_watching=self.time+self.agent.repetition_time
            if next_watching > self.agent.departure_window[1]:#too late the driver leaves
                self.agent(self.time,"alone")
                simulation.put(Travel(possible_departure,[("Od",self.agent.position),("Dd",self.agent.destination)],[[self.agent,"Od","Dd"]]))#simplify?
            else:
                simulation.put(WatchAnnounce(self.agent,next_watching))
                self.agent(self.time,"watching",position=self.agent.position)
        
class Travel(Event):
    """Has a list of points for the trajectory
    Also has the list of travellers with their start and end points"""
    def __init__(self,time,points_list,agents_list):
        """points_list -> list of tuples (point_name,point_coordinates) in the order of the travel
        agent_list -> list of list [agent,origin_name,destination_name]
                                origin_name="" if already travelling """
        self.time=time
        self.points=points_list
        self.agents=agents_list
    def __str__(self):
        out=super().__str__()+" by agents"
        for agent in self.agents:
            out+= " " + str(agent[0].id_number)
        return out
    def run(self,simulation):
        ###first lets take a look at who arrived at destination:
        start_name,start_point=self.points[0]
        finished=[]
        for passenger in self.agents:
            if passenger[1] is "" and passenger[2] is start_name:#he was moving and arrived
                passenger[0](self.time,"arrived",point=start_point)
                finished.append(passenger)
        self.agents=[x for x in self.agents if x not in finished]
        ###then lets watch if the travel is finished
        if len(self.points) is 1:#arrived to the last point -> nothing happens
            assert len(self.agents) is 0#otherwise some people were not stopped
        else:###if not the case lets identify who started and lets built the next event
            for passenger in self.agents:
                if passenger[1] is start_name:#he begins
                    passenger[1]=""
            next_name,next_point=self.points[1]
            for passenger in self.agents:
                if passenger[1] is "":#he is moving
                    passenger[0](self.time,"moving",start=start_point,end=next_point)
            travelled_time=simulation.network.travel_time(start_point,next_point)
            del self.points[0]
            simulation.put(Travel(self.time+travelled_time,self.points,self.agents))
            
            
            
            
            
#AGENTS
class Passenger(Agent):
    """ask for a drive"""
    attributes=["publishing_time","last_departure_time","position","destination"]
    def compute(self,simulation):
        simulation.put(PublishAnnounce(self))
        
class Driver(Agent):
    """propose a drive"""
    attributes=["first_watching_time","repetition_time","departure_window","position","destination","last_arrival_time","fuel_cost","time_perception"]
    def compute(self,simulation):
        simulation.put(WatchAnnounce(self,self.first_watching_time))
    def rating(self,O,D,b,n,t,*args,**kwargs):#origin and destination of passenger, benefit of taking it, network,possible departure time
        time_loss=n.travel_time(self.position,O,D,self.destination)#time of the travel if accepted
        if time_loss + t > self.last_arrival_time: # the driver refuses because he will arive too late
            return -1
        detour=n.travel_distance(self.position,O,D,self.destination)-n.travel_distance(self.position,self.destination)
        time_loss-=n.travel_time(self.position,self.destination)
        return b - detour * self.fuel_cost - time_loss * self.time_perception
    
   