import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.integrate import trapz

initial_topography = 0.005
L = 1.0  #domain length
D = 1.0  # domain depth
order = 1.0 # order of perturbation
rho = 1.0 # density
eta = 1.0 #viscosity
g = 1.0 #gravity

k = 2.0*np.pi*order/L;  #wavenumber

tau_0 = 2. * k * eta /rho / g  #reference relaxation time
tau = tau_0*(D*k + np.sinh(D*k)*np.cosh(D*k))/np.sinh(D*k)/np.sinh(D*k) #relaxation time

def generate_prm( tstep, theta):
  prmfile = open("perturb_spectrum.prm", "r")
  outfile = open("tmp.prm", "w")
  for l in prmfile.readlines():
    if 'Maximum time step' in l:
      outfile.write('set Maximum time step = %f\n'%(tstep) )
    elif 'Free surface stabilization theta' in l:
      outfile.write('  set Free surface stabilization theta = %f\n'%(theta) )
    else:
      outfile.write(l)
  prmfile.close()
  outfile.close()

def get_relaxation_times(tstep, theta):
  logfile = open("output/log.txt", "r")
  power_iteration_relaxation_time = 0
  for l in logfile.readlines():
    if 'New relaxation timescale' in l:
        power_iteration_relaxation_time = float(l.split()[4])
  analytic_relaxation_time = tau + theta*tstep
  return analytic_relaxation_time, power_iteration_relaxation_time

outputfile = open('perturb_spectrum.txt', 'w')

tsteps = np.linspace(0, 1.0, 11)[::-1]*tau
thetas = np.array([0.0, 0.5, 1.0])[::-1]

errors = []
for tstep in tsteps:
  for theta in thetas:
    print "Running with time step %f, theta %f\n"%(tstep, theta)
    generate_prm(tstep, theta)
    os.system('mpirun -n 1 /home/ian/aspect/build/aspect tmp.prm')
    analytic_relaxation_time, power_iteration_relaxation_time = get_relaxation_times(tstep, theta)
    outputfile.write("%f %f %f %f \n" % (tstep, theta, analytic_relaxation_time, power_iteration_relaxation_time) )
    outputfile.flush()

outputfile.close()
