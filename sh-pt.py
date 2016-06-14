"""Script for the execution of simulations using the 'shanghai_platform' matching system and a config.py type of parameters file."""


import argparse
import os
import sys
from importlib import import_module
from MinimalTransSim.execution import get_parameters,Write_csv, save_agents
from MinimalTransSim.shanghai_platform_extension import *
from MinimalTransSim.core import get_id



#use the parser to receive all options
parser=argparse.ArgumentParser()
parser.add_argument_group()
parser.add_argument("-p","--path",default="config.py",help="path/file of the parameters, config.py by default")
parser.add_argument("-o","--output_folder",default="data/",help="""folder for output files, data/ by default""")
detail=parser.add_mutually_exclusive_group()
detail.add_argument("-n","--no_detail",help="output files for each simulation won't be printed",action="store_true")
parser.add_argument("-f","--folder",help="""ALL NIGHT MODE: entire folder of parameters is executed, -p and -o useless, -n automatically activated (detail mode desactivated can be reactivated with -on)""")
detail.add_argument("-on",help="force the details when -f is activated",action="store_true")
args=parser.parse_args()



#define the options and the configuration list with the names of parameters files:
#usually there is only one but there is the special case of the -f option
if args.folder:#ALL NIGHT MODE (-f)
    if args.path is not "config.py":
        print("-p, --path useless")
    if args.output_folder is not "data/":
        print("-o, --output_folder useless")
    args.output_folder=args.folder
    if args.no_detail:
        print("-n, --no_detail useless")
    if args.on:
        args.no_detail=False
    else:
        args.no_detail=True
    sys.path.append(args.folder)
    configurations=[file_name[0:-3] for file_name in os.listdir(args.folder) if file_name.endswith('.py')]
else:#one file of parameter
    assert args.path.endswith('.py'),"""parameters need to be stored in .py file"""
    configurations=[args.path[0:-3]]

                 
#execution                 
for config in configurations:#each file of parameters
    try:
        parameter_file=import_module(config.replace('/','.'))#load the parameters, please note the use of import_module from importlib to avoid the top level reference used by __import__
        d=Simu_counter(config)#cretation of the displaying window
        d.start()
        name=args.output_folder#preparation of output files
        name+= config+".csv" if args.folder else "{}_{}.csv".format(get_id(),"general")
        parameter_list,variable_names=get_parameters(parameter_file)
        result_file=Write_csv(name,general_data_to_save+variable_names)
        for PARAMETERS,message in parameter_list():#for each set of parameters (vector mode)
            d.new_sim(message)#update message in displayer
            simu=create_simulation(**PARAMETERS)#creation of the simulation
            simu.set_action(lambda x: d.change(x.time))#connectino with the displaying window
            simu()#execution
            results=extract_result_data(simu)#extraction
            result_file.write(**results,**PARAMETERS)#write in the general file
            if not args.no_detail:
                save_agents(simu,args.output_folder,*particular_files)#create personal file if no_details is not activated
        d.quit()
        d.join()#wait for the displaying window to be closed
    except Exception as e:
        print(type(e).__name__," for the file '",config, "': ",e )#problem?