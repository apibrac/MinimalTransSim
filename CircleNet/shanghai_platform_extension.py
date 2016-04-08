#DRAWING SETTINGS
from CircleNet.drawing import *
from CircleNet.shanghai_platform import *

def position(agent,t,network):
    to,action=agent.story[t]
    if action[0] is "waiting" or action[0] is "watching" :
        return action[1]["position"]
    if action[0] is "matched" :
        return position(agent,to-1,network)
    if action[0] is "moving":
        D=t-to#time since last point
        D=network.distance_travelled(D)#distance made with that time
        drel=(action[1]["end"][0]-action[1]["start"][0],action[1]["end"][1]-action[1]["start"][1])#relative vector
        module=network.travel_distance((0,0),drel)#size
        dx=D*drel[0]/module#distance made in each direction
        dy=D*drel[1]/module
        return (action[1]["start"][0]+dx,action[1]["start"][1]+dy)



def create_objects(ax):
    passenger,= ax.plot([], [],'bo', ms=4)
    driver,= ax.plot([], [],'ro', ms=6)
    return [driver,passenger]

def updateFrom(simulation):
    def update(objects,t):
        p=[]
        d=[]
        for agent in simulation:
            if isinstance(agent,Passenger):
                p.append(position(agent,t,simulation.network))
            if isinstance(agent,Driver):
                d.append(position(agent,t,simulation.network))
        if p:
            x=[x[0] for x in p if x is not None]
            y=[x[1] for x in p if x is not None]
            objects[1].set_data(x,y)
        if d:
            x=[x[0] for x in d if x is not None]
            y=[x[1] for x in d if x is not None]
            objects[0].set_data(x,y)
        return objects
    return update

def Positions_drawing(simu):
    return Drawing_from_simulation(simu,create_objects,updateFrom(simu))