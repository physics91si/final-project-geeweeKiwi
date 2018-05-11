import numpy as np

class Electron:
    """Stores information about electron such as mass, energy, and wavelength"""
    
    def __init__ (self, position, velocity, mass = 9.10938356 * (10**-31)):
        """Creates electron with various parameters, posistion and velcity are np array of length 2"""
        self.h =6.62607004 * (10**-34)
        self.m = mass
        self.pos = position
        self.vel = velocity
        mag = np.sqrt(velocity.dot(velocity))#gets magnitude of velocity
        self.p = self.m * mag
        self.wvlen = self.h/self.p
        self.ke = (self.p ** 2)/2./self.m