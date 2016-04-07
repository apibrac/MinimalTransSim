# -*-coding:Latin-1 -*
"""drawing object to create animations from the simulation"""




#modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


#to write the time
def format_time(t):#in seconds
    if t//3600>0:#several hours:
        return "{}:{:02d}:{:02d}".format(int(t//3600),int((t%3600)//60),int(t%60))
    return "{:2d}:{:05.2f}".format(int(t//60),t%60)



#class for animations
class Drawing():
    def __init__(self,Xsize,Ysize,network,end,function_objects,function_update,**kargs):
        """
        Xsize,Ysize - > maximum of network
        network - > patch of the network's surface
        end - > finishing time
        function_objects - > take ax and return a LIST of drawing objects built with ax
            example :
            def create_objects(ax):
                passenger,= ax.plot([], [],'bo', ms=4)
                driver,= ax.plot([], [],'ro', ms=6)
            return [driver,passenger]
        function_update - > take the list of object and a time t, return the list of objects in their state at time t
            object[0].set_data(...)
        """
        self.X=Xsize
        self.Y=Ysize
        self.surface=network
        self.finish_time=end
        self.objects=function_objects
        self.update_from_t=function_update
        self.set_options(**kargs)
    def set_options(self,margin=20,real_size=(8,8),time_interval=10,time_coef=60,repetition=True,hide_axes=False):
        """to set options: can use default values, can be furnished when __init__ is called, can be changed (even a part of it)
        margin - > around the network
        real_size - > size of the window
        time_interval - > time between each refresh (in ms)
        time_coef - > acceleration of representation (ratio)
        repetition - > (boolean) define is the animation repeat when finished
        hide_axes - > to hide axes"""
        self.margin=margin
        self.real_size=real_size
        self.time_interval=time_interval
        self.time_coef=time_coef
        self.repetition=repetition
        self.hide_axes=hide_axes
    def update_drawing(self,ob,time_text,lt):
        def function_out(frame):
            real_time=frame*self.time_interval*self.time_coef/1000
            self.update_from_t(ob,real_time)
            rl=time.time()-lt
            time_text.set_text("In simu: "+format_time(real_time)+"\nDraw:"+format_time(frame*self.time_interval/1000)+"\nR life: "+format_time(rl))
            return tuple(ob+[time_text])
        return function_out
    def __call__(self):
        ### set the figure
        X=self.X
        Y=self.Y
        margin=self.margin
        size=((X[0]-margin,X[1]+margin),(Y[0]-margin,Y[1]+margin))
        fig=plt.figure(figsize=(self.real_size))
        ax = fig.add_axes([0,0,1,1], frameon=False, aspect=1)
        ax.set_xlim(size[0])
        ax.set_ylim(size[1])
        if self.hide_axes :
            ax.set_xticks([]), ax.set_yticks([])
        ### draw the network
        self.surface.set_facecolor('0.9')
        ax.add_patch(self.surface)
        ### create empty draw
        object_list=self.objects(ax)
        time_text = ax.text(0, 0.9, '', transform=ax.transAxes)
        ### prepare the launching
        N_frames=int(1000*self.finish_time//self.time_coef//self.time_interval+1)#why need int?
        launching_time=time.time()
        ###launch animation
        animation = FuncAnimation(fig, self.update_drawing(object_list,time_text,launching_time), interval=self.time_interval, blit=True, repeat=self.repetition, frames=N_frames)
        plt.show()
        return animation
    

#simple creator
def Drawing_from_simulation(s,o,u):#s is a simulation object
    """s= simulation - > object from system.py
        o=function_objects - > take ax and return a LIST of drawing objects built with ax
            example :
            def create_objects(ax):
                passenger,= ax.plot([], [],'bo', ms=4)
                driver,= ax.plot([], [],'ro', ms=6)
            return [driver,passenger]
        u=function_update - > take the list of object and a time t, return the list of objects in their state at time t
            object[0].set_data(...)
        """
    return Drawing(s.network.Xsize,s.network.Ysize,s.network.get_patch(),s.timer.finish_time,o,u)
