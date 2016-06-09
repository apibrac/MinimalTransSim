"""functions for all kind of draws in 2D"""


import matplotlib.pyplot as plt
from math import sqrt
import matplotlib.lines as mlines


#help for plot from a list of trajectories
def transpose(M):
    """transform M[i][j][k] in M[k][j][i]"""
    return zip(*[zip(*t) for t in zip(*M)])


    
#color determination
def color_function(m,M,cm,cM):
    """creates a function that attributes a (R,G,B) color for a value between m and M
    m has cm as a color
    M has cM
    the transformtion is linear"""
    def outf(value):
        value=(value-m)/(M-m)#between 0 and 1
        return (cm[0]*(1-value)+cM[0]*value,cm[1]*(1-value)+cM[1]*value,cm[2]*(1-value)+cM[2]*value)
    return outf
def length(trajectories):
    """length of basic travel : from first point to last one"""
    out=[]
    for t in trajectories:
        last=len(t)-1
        size=sqrt((t[0][0]-t[last][0])**2+(t[0][1]-t[last][1])**2)
        out.append(size)
    return out
def color_list(trajectories,cm,cM):
    l=length(trajectories)
    function=color_function(min(l),max(l),cm,cM)
    legend=[mlines.Line2D([], [], color=cm, markersize=15, label=str(round(min(l)))+' m'),
            mlines.Line2D([], [], color=cM, markersize=15, label=str(round(max(l)))+' m')]
    out=[]
    for v in l:
        out.append(function(v))
    return out,legend

#spatial transformations
def translation(points):
    x,y=points[0]
    return [(p[0]-x,p[1]-y) for p in points]
def rescale(points):
    x,y=points[len(points)-1]
    s=sqrt(x*x+y*y)
    return [(p[0]/s,p[1]/s) for p in points]
def turn(points):
    x,y=points[len(points)-1]
    return [(y*p[0]-x*p[1],x*p[0]+y*p[1]) for p in points]
def arrange(points):
    return turn(rescale(translation(points)))


#plot functions, from trajectory list
def plot_trajectories(trajectories):
    plt.plot(*transpose(trajectories))
    plt.axis('equal')
    plt.show()
    
def plot_relative_trajectories(trajectories,cm=(1,0.2,0),cM=(0,0.2,1)):
    colors,legend=color_list(trajectories,cm,cM)
    plt.gca().set_prop_cycle(color=colors)
    trajectories=[arrange(r) for r in trajectories]
    plt.plot(*transpose(trajectories))
    plt.axis('equal')
    plt.legend(handles=legend)
    plt.show()