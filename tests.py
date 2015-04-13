#!/usr/bin/env python3

import sirius.SI_V07 as sirius
import pyaccel
import matplotlib.pyplot as plt

# creates accelerate and inits its lattice
the_ring = sirius.create_accelerator()

# global tracking parameters
the_ring.cavity_on = True
the_ring.radiation_on = True
the_ring.vchamber_on = False


# aux. parameters and symbols
# the_ring = the_ring.lattice
num_turns, trajectory, offset = 4*512, True, 0
#
# # calcs phase space at MIA
pos = [0.001,0,0,0,0,0]
traj, turn, offset, plane = pyaccel.tracking.ringpass(the_ring, pos, num_turns, trajectory, offset)
plt.plot(1000*traj[0,:],1000*traj[1,:],'o')
plt.xlabel('x[mm]'), plt.ylabel("x'[mrad]")
# propagates from MIA to MIB
traj, offset, plane = pyaccel.tracking.linepass(the_ring, pos, trajectory, offset)
idx = pyaccel.lattice.findcells(the_ring, 'fam_name', 'mib')

# calcs phase space at MIB
pos = traj[:,idx[0]]
traj, turn, offset, plane = pyaccel.tracking.ringpass(the_ring, pos, num_turns, trajectory, offset=idx[0])
plt.plot(1000*traj[0,:],1000*traj[1,:],'o')
plt.xlabel('x[mm]'), plt.ylabel("x'[mrad]")

plt.show()
