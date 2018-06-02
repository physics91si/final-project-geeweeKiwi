import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
import barrier
import electron
from random import random


def main():
    num = 10
    height = 50
    E_max = 20
    E_min = None
    barr = .5*10**-10
    mass = 9.10938356 * (10**-31)
    args = sys.argv[1:]
    print args
    if len(args) == 1:
        num = int(args[0])
    if len(args) == 2:
        num = int(args[0])
        height = float(args[1])
    if len(args) == 3:
        num = int(args[0])
        height = float(args[1])
        E_max = float(args[2])
    if len(args) == 4:
        num = int(args[0])
        height = float(args[1])
        E_max = float(args[2])
        E_min = float(args[3])
    if len(args) == 5:
        num = int(args[0])
        height = float(args[1])
        E_max = float(args[2])
        E_min = float(args[3])
        barr = 10**float(args[4])
    if len(args) == 6:
        num = int(args[0])
        height = float(args[1])
        E_max = float(args[2])
        E_min = float(args[3])
        barr = float(args[4])*(10**int(args[5]))                          
    if len(args) == 7:
        num = int(args[0])
        height = float(args[1])
        E_max = float(args[2])
        E_min = float(args[3])
        barr = float(args[4])*(10**int(args[5]))
        mass = mass * float(args[6])
    n = 10
    dt = 1./20.*np.sqrt(mass/(2*convertEv(E_max)))
    run_dynamics(n, dt, num, height, E_max, E_min, barr, mass)

def convertEv(n):
    return n*1.6022e-19

def init_electrons(num, E_max, E_min, mass):
    ''' initializes array of electrons of length num with energies in range E_min to E_max, if no E_min is given, all electrons will have energy E_max, if neither, all will have E = 20 '''
    if E_min == None:
        E_min = E_max
    E_min = convertEv(E_min)
    E_max = convertEv(E_max)
    energies = np.array([E_min + (E_max - E_min)*(random()) for i in range (0, num)])
    positions = np.array([np.array([random(), random()]) for i in range (0, num)])
    directions = []
    for i in range(0, num):
        rand_ang = 2*np.pi*random()
        directions.append(np.array([np.cos(rand_ang), np.sin(rand_ang)]))
    directions = np.array(directions)
    electron_list = []
    for i in range(0, num):
        electron_list.append(electron.Electron(positions[i], directions[i], energies[i], mass))
    
    return np.array(electron_list)
    
def init_barriers(height, width):
    height = convertEv(height)
    return np.array([barrier.Barrier(height, width) for i in range(0,4)])
    
    
def time_step(dt, electrons, barriers):
    """Sets new positions and check for tunneling of electrons"""
    for electron in electrons:
        electron.pos += electron.vel*dt
        electron.t += dt
        x = electron.pos[0]
        y = electron.pos[1]
        if x > 1:
            tunnel = barriers[0].does_escape(electron)
            electron.pos[0] = 1
            if tunnel:
                print "electron escaped at position: ", electron.pos, " and time: ", electron.t
                electron.tf = electron.t
                electron.vel = np.array([0,0])
            else:
                electron.vel[0] = -1*electron.vel[0]
        if y > 1:
            tunnel = barriers[1].does_escape(electron)
            electron.pos[1] = 1
            if tunnel:
                print "electron escaped at position: ", electron.pos, " and time: ", electron.t
                electron.tf = electron.t
                electron.vel = np.array([0,0])
            else:
                electron.vel[1] = -1*electron.vel[1]
        if x < 0:
            tunnel = barriers[2].does_escape(electron)
            electron.pos[0] = 0
            if tunnel:
                print "electron escaped at position: ", electron.pos, " and time: ", electron.t
                electron.tf = electron.t
                electron.vel = np.array([0,0])
            else:
                electron.vel[0] = -1*electron.vel[0]
        if y < 0:
            tunnel = barriers[3].does_escape(electron)
            electron.pos[1] = 0
            if tunnel:
                print "electron escaped at position: ", electron.pos, " and time: ", electron.t
                electron.tf = electron.t
                electron.vel = np.array([0,0])
            else:
                electron.vel[1] = -1*electron.vel[1]
                
    for electron in electrons:
        if electron.vel.any() != 0:
            return True    
    print "simulation ended at t =", electrons[0].t, "sec"
    total_time = 0
    for electron in electrons:
        total_time += electron.tf
    avg_tunnel_time = total_time/len(electrons)
    print "average tunnel time was: ", avg_tunnel_time, "sec"
    return False
                
def run_dynamics(n, dt, num, height, E_max, E_min, barr, mass, xlim=(0, 1), ylim=(0, 1)):
    """Calculate each successive time step and animate it"""
    barriers = init_barriers(height, barr)
    electrons = init_electrons(num, E_max, E_min, mass)

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
    label = mpatches.Patch(color = None, label='dt = %s' % float('%.3g' % dt))
    plt.legend(handles=[label],loc='upper right', bbox_to_anchor=(1, 1))
    plt.xlabel(r'$x$')
    plt.ylabel(r'$y$')
    plt.title('Electron Tunneling Simulation')
    dynamic_ani = animation.FuncAnimation(fig, update_anim, n, fargs=(dt, electrons, barriers,line), interval=50, blit=False)
    plt.show()
                

def update_anim(i, dt, electrons, barriers, line):
    """Update and draw the molecule. Called by FuncAnimation"""
    is_not_over = time_step(dt, electrons, barriers)
    
    elecs_xpos = []
    elecs_ypos = []
    for e in electrons:
        elecs_xpos.append(e.pos[0])
        elecs_ypos.append(e.pos[1])
    
    if is_not_over:
        line.set_data(tuple(elecs_xpos), tuple(elecs_ypos))
        return line,
    else: plt.close()

if __name__ == '__main__': main()
    # Set the number of iterations and time step size
   

