import numpy as np
from random import random
import electron

class Barrier:
    """Stores information about barrier such as, energy height and and width"""
    
    def __init__ (self, height, width):
        self.U0 = height
        self.L = width
        self.h_bar = (6.62607004 * (10**-34))/(2.*np.pi)
        
    def does_escape(self, elec):
        if self.U0 > elec.ke:
            k = np.sqrt(2*elec.m*(self.U0 - elec.ke)) / self.h_bar
            p = np.exp(-2*k*self.L)
            #print(p)
            num = random()
            if num > p:
                return False
        return True