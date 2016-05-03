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

-for relevent data extraction:
extract_result_data(s)
otherwise the extraction/observation function should be re implemented manually (way more easy)
"""

import CircleNet.animation
import CircleNet.draws
import CircleNet.shape as sh
import CircleNet.system as sys
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



# FOR ROUTE PLOT
def plot_routes(simu):
    P=driver_matched_route_extraction(simu)
    CircleNet.draws.plot_trajectories(P)
def plot_relative_routes(simu,cm=(1,0.2,0),cM=(0,0.2,1)):
    P=list(driver_matched_route_extraction(simu))
    CircleNet.draws.plot_relative_trajectories(P,cm,cM)
    
    

    
# DATA EXTRACTION
#route
def extract_route(driver):
    route=[]
    for _,action in driver.story.reverse_iter():
        if action[0] is "moving" :
            route.append(action[1]["start"])
        elif action[0] is "arrived":
            route.append(action[1]["point"])
    return route
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
                points.append(extract_route(agent))
    return points
#egeneral info
def nb_driver_passenger_match(simu):
    matchD,numberD,matchP,numberP=0,0,0,0
    for p in simu:
        if isinstance(p,platform.Driver):
            numberD+=1
            if p.story.get_attribute("matched")[0] is 1:
                matchD+=1
        if isinstance(p,platform.Passenger):
            numberP+=1
            if p.story.get_attribute("matched")[0] is 1:
                matchP+=1
    assert matchP == matchD, """not same number of pedestrian and driver matched,
    this assertion is not nececessary, is here
    as long as the match is one to one, to be deleted otherwise"""
    return numberD,numberP,matchP
def vks_average_total(simu):
    l=[agent.story.get_attribute("vks")[0] for agent in simu if isinstance(agent,platform.Driver)]
    l=[e for e in l if e is not ""]
    return sum(l)/len(l),sum(l)
def waiting_average(simu):
    l=[agent.story.get_attribute("waiting")[0] for agent in simu if isinstance(agent,platform.Passenger)]
    l=[e for e in l if e is not ""]
    return sum(l)/len(l)



def extract_result_data(simu,parameters={}):#data already gather parameters
    """has results extracted from the simulation, can integrate parameters"""
    data={}
    data["average_waiting_time"]=waiting_average(simu)
    data["average_vks"],data["total_vks"]=vks_average_total(simu)
    data["nb_driver"],data["nb_passenger"],data["nb_match"]=nb_driver_passenger_match(simu)
    data["driver_efficiency"]=data["nb_match"]/data["nb_driver"]
    data["passenger_efficiency"]=data["nb_match"]/data["nb_passenger"]
    data["execution_time"]=simu.execution_time
    data["id_sim"]=simu.id_sim
    data.update(parameters)
    return data




#SIMULATION CREATOR
def create_simulation(speed,radius,end,first_watching_before_first_departure,window_size_of_departure,
                       time_elasticity,fuel_cost,watching_repetition_average,watching_repetition_variance,
                      time_perception_average,time_perception_variance,publishing_advance,benefits,N_driver,N_passenger):
    #random functions
    watching_repetition=sh.get_log_normal(watching_repetition_average,watching_repetition_variance)
    time_perception=sh.get_log_normal(time_perception_average,time_perception_variance)
    #agents generator
    def SimpleDriver(simulation):
        t=simulation.timer.random_time()
        O=simulation.network.position_generator()
        D=simulation.network.position_generator()
        w=(t+first_watching_before_first_departure,t+first_watching_before_first_departure+window_size_of_departure)
        A=w[1]+simulation.network.travel_time(O,D)+time_elasticity
        return platform.Driver(first_watching_time=t,
                      repetition_time=watching_repetition(),
                      departure_window=w,
                      position=O,destination=D,
                      last_arrival_time=A,
                      fuel_cost=fuel_cost,
                      time_perception=time_perception())
    def SimplePassenger(simulation):
        t=simulation.timer.random_time()
        O=simulation.network.position_generator()
        D=simulation.network.position_generator()
        return platform.Passenger(publishing_time=t,
                         last_departure_time=t+publishing_advance,
                         position=O,destination=D)
    N=sh.circle(radius,speed)
    T=sh.Timer(end)
    simu=sys.Simulation(N,T)
    simu.matchingAlgo=platform.MatchingPlatform(benefits,simu)
    for i in range(N_driver):
        simu.add(SimpleDriver(simu))
    for i in range(N_passenger):
        simu.add(SimplePassenger(simu))
    return simu