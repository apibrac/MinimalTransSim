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


