"""drawing elements for a simulation of type CircleNet.shanghai_platform

if s of type Simulation, execute:
-for an animation:
dr=Positions_drawing(s)
dr.set_options(margin=20,real_size=(10,10),time_interval=30,time_coef=1000,repetition=True,hide_axes=True)#optional
dr()

-for a plot of deviated route:
plot_routes(s)

-for a relative plot of deviated route:
plot_relative_routes(s)
"""

import CircleNet.animation
import CircleNet.draws
import CircleNet.shanghai_platform as platform

# FOR ANIMATION :

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
            if isinstance(agent,platform.Passenger):
                p.append(position(agent,t,simulation.network))
            if isinstance(agent,platform.Driver):
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
    return CircleNet.animation.Drawing_from_simulation(simu,create_objects,updateFrom(simu))


# FOR DEVIATED TRAJECTORIES :

#data extraction
def driver_matched_route_extraction(simu):
    points=[]
    for agent in simu:
        if isinstance(agent,platform.Driver):
            interesting=False
            for _,action in agent.story:
                if action[0] is "matched":#we want his route !
                    interesting=True
                    break
            if interesting :
                route=[]
                for _,action in agent.story.reverse_iter():
                    if action[0] is "moving" :
                        route.append(action[1]["start"])
                    elif action[0] is "arrived":
                        route.append(action[1]["point"])
                points.append(route)
    return points


#route plot functions
def plot_routes(simu):
    P=driver_matched_route_extraction(simu)
    CircleNet.draws.plot_trajectories(P)
    
def plot_relative_routes(simu,cm=(1,0.2,0),cM=(0,0.2,1)):
    P=list(driver_matched_route_extraction(simu))
    CircleNet.draws.plot_relative_trajectories(P,cm,cM)