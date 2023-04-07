import numpy as np
import matplotlib.pyplot as plt
import pylab
from matplotlib.patches import Ellipse
import numpy.random as rnd
from mpl_toolkits.mplot3d import Axes3D

def power_display(x_leader, y_leader, x_tier1, y_tier1, x_tier2, y_tier2, x_tier3, y_tier3, x_policy, y_policy, x_no, y_no):
    fig = plt.figure(0)
    ax = fig.add_subplot(111, aspect='equal')
    e_leader = Ellipse(xy = (x_leader,y_leader), width = 1, height = 1, angle = 180)
    # e_tier1 = [Ellipse(xy = (x_tier1[i],y_tier1[i]), width = x_tier1[i].influence[0], height = x_tier1[i].influence[1], angle = 90) for i in range(len(x_tier1))]
    # e_tier2 = [Ellipse(xy = (x_tier2[i],y_tier2[i]), width = x_tier2[i].influence[0], height = x_tier2[i].influence[1], angle = 360) for i in range(len(x_tier2))]
    # e_tier3 = [Ellipse(xy = (x_tier3[i],y_tier3[i]), width = x_tier3[i].influence[0], height = x_tier3[i].influence[1], angle = 180) for i in range(len(x_tier3))]
    e_tier1 = [Ellipse(xy = (x_tier1[i],y_tier1[i]), width = 0.5, height = 1, angle = 90) for i in range(len(x_tier1))]
    e_tier2 = [Ellipse(xy = (x_tier2[i],y_tier2[i]), width = 1, height = 0.5, angle = 360) for i in range(len(x_tier2))]
    e_tier3 = [Ellipse(xy = (x_tier3[i],y_tier3[i]), width = 0.25, height = 0.5, angle = 180) for i in range(len(x_tier3))]

    ax.add_artist(e_leader)
    e_leader.set_facecolor("red")
    for e in e_tier1:
        ax.add_artist(e)
        e.set_facecolor("black")
    for e in e_tier2:
        ax.add_artist(e)
        e.set_facecolor("black")
    for e in e_tier3:
        ax.add_artist(e)
        e.set_facecolor("blue")

    ax.plot(x_policy, y_policy, marker='s', color='green', markersize = 10)

    #leader与tier1-agent一直连着线 
    plt.plot([x_leader, x_no[0]],[y_leader, y_no[0]])
    plt.plot([x_leader, x_no[1]],[y_leader, y_no[1]])
    plt.ylim(ymax=11,ymin=0)
    plt.xlim(xmax=11,xmin=0)
    plt.title("Power Display")

    plt.show()

def agent_stats(leader_utility,aggregate_support):
    fig = plt.figure(1)
    ax = fig.add_subplot(111, aspect='equal')
    x = [0.05*(i+1) for i in range(200)]
    plt.plot(x, leader_utility, c="red")
    plt.plot(x, aggregate_support, c="blue")

    plt.grid(True)
    plt.ylim(ymax=11,ymin=5)
    #plt.xlim(xmax=10,xmin=0)
    plt.legend(labels=['Leader utility', 'Aggregate support for the regime'], loc='lower right')
    plt.title("Agent Stats")
    plt.show()

def utility_3D(x_policy, y_policy, leader_utility):
    fig = plt.figure(3)
    ax = fig.add_subplot(111, projection='3d')

    # Make data

    # Plot the surface
    #ax.plot_surface(x, y, z, color='b')
    ax.plot_surface(x_policy, y_policy, leader_utility, cmap='rainbow')

    plt.show()
