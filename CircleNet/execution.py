"""gather all functions for execution of a simulation (managemenet of parameters,"""






#PARAMETERS READER
def extract(module):
    static={}
    variable={}
    for key in module.__dir__():
        if "__" not in key:
            if key[0] is "V":
                variable[key[1:]]=module.__dict__[key]
            else:
                static[key]=module.__dict__[key]
    return static,variable
def get_parameter_sets(message,static,**variable):
    if not variable:#everything is static
        yield static,message
        raise StopIteration
    key,new_variable = variable.popitem()# new_variable is the list of values that key should take
    for value in new_variable:
        static[key]=value
        submessage=message+str(key)+"="+str(value)+" "
        for out in get_parameter_sets(submessage,static,**variable):
            #send all outputs generated from variable that stay with the current value of key
            yield out           
def get_parameters(module_name):
    s,v=extract(module_name)
    return get_parameter_sets("",s,**v)




#FILE WRITTERS
class Write_csv():
    def __init__(self,name,keys_to_save):
        self.file_name=name
        self.the_string="{"+"},{".join(keys_to_save)+"}\n"
        with open(self.file_name , "w") as file :
            file.write(",".join(keys_to_save)+"\n")#write the first line
            assert len(keys_to_save)>0, "nothing to save"
    def write(self,**values):
        with open(self.file_name , "a") as file :
            file.write(self.the_string.format(**values))
            

#for agents
def extract_info(agent, attributes_list, options_name={}):
    """look for the attributes_list of agent and store it in dictionary
    first look in the agent object and if its not found, look in the story object
    
    options_name can be filled with key, attributes , where the list attributes will receive the values of key in agent or story
    can be used to change the name of an attribute or to cut an attribute in two (for example options_name['position']=(x,y))"""
    out={}
    for att in attributes_list:
        if hasattr(agent,att):
            out[att]=agent.__dict__[att]
        else :
            out[att]=agent.story.get_attribute(att)[0]#it's a list
    for key in options_name:
        l=[]
        if hasattr(agent,key):
            l=agent.__dict__[key]
        else :
            l=agent.story.get_attribute(key)[0]#it's a list
        if isinstance(options_name[key],tuple):#l need to be a list
            out.update(dict(zip(options_name[key],l)))
        else :# l is the object
            out[options_name[key]]=l
    return out
def save_agents(simu,*files_info):
    """every file in files_info is a dictionnary
        file[name] -> name of the output file (preceded by {id}_)
        file[selection_function] -> send true for all agents concerned by this file
        file[info_list] -> list of info to store
        file[options_list] -> optional to give the provenance of several info (see extract_info)"""
    for file in files_info:
        file["writter"]=open("data/{}_{}.csv".format(simu.id_sim,file["name"] ),"w")
        file["writter"].write(",".join(file["info_list"])+"\n")
        file["the_string"]="{"+"},{".join(file["info_list"])+"}\n"
    for agent in simu:
        for file in files_info:
            if file["selection_function"](agent):
                data=extract_info(agent,file["info_list"],file.get("options_list",{}))#options_list is optional
                file["writter"].write(file["the_string"].format(**data))
    for file in files_info:
        file["writter"].close()
    

