import numpy as np

class Electron:
    """Stores information about electron such as mass, energy, and wavelength"""
    
    def __init__ (self, position, direction, energy, mass = 9.10938356 * (10**-31)):
        """Creates electron with various parameters, posistion and direction are np array of length 2, direction should be a unit vectore"""
        self.h = 6.62607004 * (10**-34)
        self.m = mass
        self.pos = position
        mag = np.sqrt(2 * energy/self.m)#gets magnitude of velocity
        #n = len(mag)
        self.vel = direction*mag
        
        #for i in range (0, n):
            #self.vel[i] = direction[i] * mag[i]
        
        self.p = self.m * mag
        self.wvlen = self.h/self.p
        self.ke = energy