# Minimal Transportation Simulation

Simulation platform to model, simulate and analyse dynamic transportation systems (such as dynamic ridesharing, taxi or float of driverless car) and their users.

## Intro

The purpose of the tool is to model dynamic transportation systems (systems that involve a matching process between cars and passengers, making the car unavalaible for other users).
The approach is minimalist: the network, the matching system and the different users are simplified as much as possible.
It is event-based.

Intended results are analysis of reliability and efficiency of the studied matching platform for different kind of users or different global parameters (prices, average speed, number of users etc).

## Implemeted parts

The core system is implemented. It needs a choice and an implementation of a matching platform to be launched.
One matching platform is implemented (inspired by Didi, Shanghai). It only needs a set of parameters to be implemented.

## How to use

### Ready to use

A transportation system is already implemented. It is inspired by the Didi application of Shanghai. It only requires different parameters to be executed and analysed.

1) The simplest way is to choose and change the parameters located in the config.py file(see next paragraph). Then, the execution of sh-pt.py will launch the simulation and place the results in the data folder.
A window ('tk') is opened to show the state of the current simulation.
Three files are created: "drivers" and "passengers" gathered all information of the agents, "general" has general information on the system.

2)  01_shanghai_platform is jupyter notebook that executes the same simulation than sh_pt.py (using the config.py file) but other general parameters can be manually changed and some visualization tool are available.

3) sh_pt.py can be launched has a command line using different arguments (see -h for the description of all them). Especially the --folder option can be usefull for heavy simulations.

### Parameterisation

Usually the parameters are located in the config.py file. They can be located in another file with the same template.
The list of possible parameters is explicit. They can easily be understood and changed to see their impact in the results.

Vector mode:
If one wants to launch several simulations with different values for the same parameter, one can give to the parameter a vector of values instead of one unique value, and preceed the name of the parameter by "V".
In such case, one simulation will be launched for every value of the parameter. The tk window show what simulation is currently launched.
"drivers" and "passengers" files are created for every simulation (if they are useless, the --no_detail option is here to avoid them and save memory).
Only one "general" file is created: each line is one of the simulation with its particular results and with the value of the changed parameters.
Several parameters can be put in vector mode in the same time. Please note that every simulation with every possible configurations of parameters will be launched. It means it can be a very high number of one put more than two parameters in vector mode.
Example:
N_driver= 2000 //launch one simulation with 2000 drivers
VN_driver= [2000,4000,5000] //launch three simulation with respectively 2000, 4000 and 5000 dirvers

### Analysis

### New transportation systems
