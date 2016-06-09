"""File with all parameters for a simulation
Units used are SI : meter and second
Calculation of variable, defenition of function etc can be made here

If a parameter needs to take several values, put them in a list and preceed the parameter with 'V' (which will be removed)
    example Vnumber_of_drivers=[1000,2000] means the parameter number_of_drivers will take both the values 1000 and 2000
If several parameters are variable in this way, all possible configurations of them will be executed"""




#DIMENSION OF THE NETWORK 
speed = 25 / 3.6 # 25 km/h
radius = 25 * 1000 #  25km
end = 3 * 3600 #  3h

#GENERAL VALUES
N_driver=2000# [100000]# [2000,4000,5000]#,6000,7000,8000,9000,10000,20000,30000,50000]
N_passenger=2000#[100000]# [2000,4000,5000]#,6000,7000,8000,9000,10000,20000,30000,50000]

#DRIVERS CARACTERISTICS
first_watching_before_first_departure = 5 * 60
window_size_of_departure = 15 * 60
time_elasticity = 5 * 60
fuel_cost = 0.6/1000#0.5RMB per kilometer
watching_repetition_average = 60 # -> random
watching_repetition_variance = 10
time_perception_average = 5/60 # = 24 * 50/100 / 3600 #50% of average income, in second   -> random
time_perception_variance = 3/60 #10% percent

#PASSENGERS CARACTERISTICS
publishing_advance = 20 * 60
    
#PLATFORM CARACTERISTICS
def benefits(origin,destination,network):
    """Shanghai pricing"""
    distance=network.travel_distance(origin,destination) / 1000 # in meter
    if distance < 3: #3 first km fixprice
        return 11#in RMB
    if distance < 20:#until 20km at 1.5RMB / km
        return 6.5 + distance * 1.5 # 11 + (distance - 3) * 1.5
    return 16.5 + distance # 28.5 + (distance - 20) *1   # 28.5 = 3 + (20 - 3) * 1.5