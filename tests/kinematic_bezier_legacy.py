# -*- coding: utf-8 -*-
# Copyright (C) 2013 Quang-Cuong Pham <cuong.pham@normalesup.org>
#
# This file is part of the Time-Optimal Path Parameterization (TOPP) library.
# TOPP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
sys.path.append('..')

import TOPPbindings
import TOPPpy
import time
import string
from pylab import *
from numpy import *


ion()

#random.seed(0)

############################ Tunings ############################
discrtimestep = 0.001
integrationtimestep = discrtimestep
reparamtimestep = 0#auto
passswitchpointnsteps = 5
tuningsstring = "%f %f %f %d"%(discrtimestep,integrationtimestep,reparamtimestep,passswitchpointnsteps)


############################ Trajectory ############################
#------------------------------------------#
# p0v = [[1,1],[1,1]]
# p1v = [[0.3,1.3],[1,2]]
# p2v = [[1,0],[0.3,1.3]]
# p3v = [[1,1],[1,1]]
# p0v = [[1,1,0],[1,1,0]]
# p1v = [[0.3,1.3,1],[1,2,-1]]
# p2v = [[1,0,1],[0.3,1.3,0]]
# p3v = [[1,1,0],[1,1,1]]
# Tv = [0.5,0.5]

ndof = 2
p0v = [rand(ndof)*2*pi-pi]
p1v = [rand(ndof)*2*pi-pi]
p2v = [rand(ndof)*2*pi-pi]
p3v = [rand(ndof)*2*pi-pi]
Tv = [1]
trajectorystring="""1
2
1.000000 -4.476723 -4.127280 4.327536
1.000000 -10.662396 12.189375 -4.581347"""
#trajectorystring = TOPPpy.BezierToTrajectoryString(Tv,p0v,p1v,p2v,p3v)

print trajectorystring

#------------------------------------------#
traj0 = TOPPpy.PiecewisePolynomialTrajectory.FromString(trajectorystring)


############################ Constraints ############################
#------------------------------------------#
amax = 1*ones(ndof)
vmax = 1*ones(ndof)
t0 = time.time()
constraintstring = string.join([str(v) for v in amax]) + "\n"
constraintstring += string.join([str(v) for v in vmax])
#------------------------------------------#


############################ Run TOPP ############################
t1 = time.time()
x = TOPPbindings.TOPPInstance("KinematicLimits",constraintstring,trajectorystring,tuningsstring);
t2 = time.time()
ret = x.RunComputeProfiles(0,0)
t3 = time.time()

if(ret == 1):
    x.ReparameterizeTrajectory()

t4 = time.time()

################ Plotting the MVC and the profiles #################
x.WriteProfilesList()
x.WriteSwitchPointsList()
profileslist = TOPPpy.ProfilesFromString(x.resprofilesliststring)
switchpointslist = TOPPpy.SwitchPointsFromString(x.switchpointsliststring)
TOPPpy.PlotProfiles(profileslist,switchpointslist,4)


##################### Plotting the trajectories #####################
if(ret == 1):
    x.WriteResultTrajectory()
    traj1 = TOPPpy.PiecewisePolynomialTrajectory.FromString(x.restrajectorystring)
    TOPPpy.PlotKinematics(traj0,traj1,0.01,vmax,amax)


print "\n--------------"
print "Python preprocessing: ", t1-t0
print "Building TOPP Instance: ", t2-t1
print "Compute profiles: ", t3-t2
print "Reparameterize trajectory: ", t4-t3
print "Total: ", t4-t0
print "Trajectory duration (estimate): ", x.resduration
if(ret == 1):
    print "Trajectory duration: ", traj1.duration
    print "Trajectory 0 nsteps: ", len(traj0.chunkslist)
    print "Trajectory 1 nsteps: ", len(traj1.chunkslist)


# data=loadtxt('/home/cuong/Downloads/mintos/examples/res')
# tvect = data[:,0]
# xvect = data[:,2]
# yvect = data[:,3]

# dt2 = tvect[1]-tvect[0]
# figure(0)
# plot(tvect,xvect,'m')
# plot(tvect,yvect,'c')
# figure(1)
# plot(tvect[:-1],diff(xvect)/dt2,'m')
# plot(tvect[:-1],diff(yvect)/dt2,'c')
# figure(2)
# plot(tvect[:-2],diff(diff(xvect))/dt2/dt2,'m')
# plot(tvect[:-2],diff(diff(yvect))/dt2/dt2,'c')

raw_input()
