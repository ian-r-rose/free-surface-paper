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

k_s = 2.0*np.pi/L;  #wavenumber
k = 2.0*np.pi*order/L;  #wavenumber

tau_0 = 2. * k * eta /rho / g  #reference relaxation time
tau = tau_0*(D*k + np.sinh(D*k)*np.cosh(D*k))/np.sinh(D*k)/np.sinh(D*k) #relaxation time

tau_0s = 2. * k_s * eta /rho / g  #reference relaxation time
tau_s = tau_0s*(D*k_s + np.sinh(D*k_s)*np.cosh(D*k_s))/np.sinh(D*k_s)/np.sinh(D*k_s) #relaxation time

def analytic_solution( t ):
  return initial_topography * np.exp(-t/tau)

def generate_prm( tstep, relax ):
  prmfile = open("relaxation.prm", "r")
  outfile = open("tmp.prm", "w")
  for l in prmfile.readlines():
    if 'Maximum time step' in l:
      outfile.write('set Maximum time step = %f\n'%(tstep) )
    elif 'End time' in l:
      outfile.write('set End time = %f\n'%(4.0*tau) )
    elif 'Time between graphical' in l:
      outfile.write('    set Time between graphical output = %f\n'%(tau/10.) )
    elif 'Relaxation time' in l:
      outfile.write('    set Relaxation time = %f\n'%(relax) )
    elif 'Amplitude' in l:
      outfile.write('    set Amplitude = %f\n'%(initial_topography) )
    elif 'Order' in l:
      outfile.write('    set Order = %f\n'%(order) )
    else:
      outfile.write(l)
  prmfile.close()
  outfile.close()


def calculate_error():
  data = np.genfromtxt("output/statistics", usecols = (1,9,11) )
  time = data[:,0]
  tstep = data[:,1]
  topo = -data[:,2]

  #compute l2 difference between the output and the analtic solution
  error = np.sqrt(np.power( (topo-analytic_solution(time))/initial_topography, 2.))
  #integrate in time, divide by the total time
  cumulative_error = trapz(error, time)/time[-1]
  return cumulative_error

def plot_topography():
  data = np.genfromtxt("output/statistics", usecols = (1,9,11) )
  time = data[:,0]
  tstep = data[:,1]
  topo = -data[:,2]

  plt.plot(time, topo)
  plt.plot(time, analytic_solution(time) )
  plt.show()
  plt.clf()
  


outputfile = open('tau_sensitivity.txt', 'w')
tsteps = [0.1*tau_s,]
relaxation_times = np.linspace(0.1, 2.0, 96)*tau_s
errors = []
for r in relaxation_times:
  for t in tsteps:
    print "Running with time step %f, relaxation time %f\n"%(t, r)
    generate_prm(t, r)
    os.system('mpirun -n 4 /home/ian/aspect/build/aspect tmp.prm')
    #plot_topography()
    outputfile.write("%f %f %f \n" % (r/tau_s, t/tau_s, calculate_error()) )
    outputfile.flush()
outputfile.close()
