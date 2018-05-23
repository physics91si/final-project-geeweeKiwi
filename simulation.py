import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import barrier
import electron
from random import random


def init_electrons(num = 10, E_min = None, E_max = 20):
    ''' initializes array of electrons of length num with energies in range E_min to E_max, if no E_min is given, all electrons will have energy E_max, if neither, all will have E = 20 '''
    if E_min == None:
        E_min = E_max
    energies = np.array([E_min + (E_max - E_min)*(random()) for i in range (0, num)])
    positions = np.array([np.array([random(), random()]) for i in range (0, num)])
    rand_ang = 2*np.pi*random()
    directions = np.array([np.array([np.cos(rand_ang), np.sin(rand_ang)]) for i in range (0, num)])
    
    electron_list = []
    for i in range(0, num):
        electron_list.append(electron.Electron(positions[i], directions[i], energies[i]))
    
    return np.array(electron_list)
    
def init_barriers(height = 50, width = 10**-20):
    return np.array([barrier.Barrier(height, width) for i in range(0,4)])
    
    
def time_step(dt, electrons, barriers):
    """Sets new positions and check for tunneling of electrons"""
    for electron in electrons:
        electron.pos += electron.vel*dt
        x = electron.pos[0]
        y = electron.pos[1]
        if x > 1:
            tunnel = barriers[0].does_escape(electron)
            electron.pos[0] = 1
            if tunnel:
                print "electron escaped at position: ", electron.pos
                electron.vel = np.array([0,0])
            else:
                electron.vel[0] = -1*electron.vel[0]
        if y > 1:
            tunnel = barriers[1].does_escape(electron)
            electron.pos[1] = 1
            if tunnel:
                print "electron escaped at position: ", electron.pos
                electron.vel = np.array([0,0])
            else:
                electron.vel[1] = -1*electron.vel[1]
        if x < 0:
            tunnel = barriers[2].does_escape(electron)
            electron.pos[0] = 0
            if tunnel:
                print "electron escaped at position: ", electron.pos
                electron.vel = np.array([0,0])
            else:
                electron.vel[0] = -1*electron.vel[0]
        if y < 0:
            tunnel = barriers[3].does_escape(electron)
            electron.pos[1] = 0
            if tunnel:
                print "electron escaped at position: ", electron.pos
                electron.vel = np.array([0,0])
            else:
                electron.vel[1] = -1*electron.vel[1]
                
def run_dynamics(n, dt, xlim=(0, 1), ylim=(0, 1)):
    """Calculate each successive time step and animate it"""
    barriers = init_barriers()
    electrons = init_electrons()

    # Animation stuff
    fig, ax = plt.subplots()
    
    elecs_xpos = []
    elecs_ypos = []
    for e in electrons:
        elecs_xpos.append(e.pos[0])
        elecs_ypos.append(e.pos[1])
    
    
    line, = ax.plot(tuple(elecs_xpos), tuple(elecs_ypos), 'o')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    plt.title('Electron Tunneling Simulation')
    dynamic_ani = animation.FuncAnimation(fig, update_anim, n, fargs=(dt, electrons, barriers,line), interval=50, blit=False)
    plt.show()
                

def update_anim(i, dt, electrons, barriers, line):
    """Update and draw the molecule. Called by FuncAnimation"""
    time_step(dt, electrons, barriers)
    
    elecs_xpos = []
    elecs_ypos = []
    for e in electrons:
        elecs_xpos.append(e.pos[0])
        elecs_ypos.append(e.pos[1])
    
    line.set_data(tuple(elecs_xpos), tuple(elecs_ypos))
    return line,

if __name__ == '__main__':
    # Set the number of iterations and time step size
    n = 10
    dt = 10**-18
    run_dynamics(n, dt)