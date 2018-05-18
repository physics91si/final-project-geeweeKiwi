import sys
import matplotlib.pyplot as plt
import maplotlib.animation as animation
import numpy as np
import barrier as br
import electron as ec
import random


def init_electrons(num = 100, E_min = None, E_max = 20):
    ''' initializes array of electrons of length num with energies in range E_min to E_max, if no E_min is given, all electrons will have energy E_max, if neither, all will have E = 20 '''
    if E_min == None:
        E_min = E_max
    energies = np.array([E_min + (E_max - E_min)*(random()) for i in range (0, num)])
    positions = np.array([np.array([random(), random()]) for i in range (0, num)])
    rand_ang = 2*np.pi*random()
    directions = np.array([np.array([np.cos(rand_ang), np.sin(rand_ang)]) for i in range (0, num)])
    return electron.Electron(positions, directions, energies)
    
def init_barriers(height = 25, width = 10**-20):
    return np.array([barrier.Barrier(height, width) for i in range(0,4)])
    
    
def time_step(dt, electrons, barriers):
    """Sets new positions and check for tunneling of electrons"""
    electrons.pos += electrons.vel*dt
    for electron in electrons:
        x = electron.pos[0]
        y = electron.pos[1]
        if x > 1:
            tunnel = barrier[0].does_escape(electron)
            electron.pos[0] = 1
            if tunnel:
                print "electron escaped at position: ", electron.pos
            else:
                electron.vel[0] = -1*electron.vel[0]
        if y > 1:
            tunnel = barrier[1].does_escape(electron)
            electron.pos[1] = 1
            if tunnel:
                print "electron escaped at position: ", electron.pos
            else:
                electron.vel[1] = -1*electron.vel[1]
        if x < 0:
            tunnel = barrier[2].does_escape(electron)
            electron.pos[0] = 0
            if tunnel:
                print "electron escaped at position: ", electron.pos
            else:
                electron.vel[0] = -1*electron.vel[0]
        if y < 0:
            tunnel = barrier[3].does_escape(electron)
            electron.pos[1] = 0
            if tunnel:
                print "electron escaped at position: ", electron.pos
            else:
                electron.vel[1] = -1*electron.vel[1]
                
