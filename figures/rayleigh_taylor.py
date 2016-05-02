import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import itertools

try:
  plt.style.use('./free_surface_paper.mplstyle')
except AttributeError:
  print "old matplotlib version?"
except ValueError:
  print "Cannot find the requested stylesheet"

prefix = '../benchmarks/rayleigh_taylor/'

#Load in datasets
skip = 20
forward_euler = np.genfromtxt(prefix+'output_small_time_step/statistics', skip_header=skip, usecols=(1,15))[::10]
nsfd_adaptive_02 = np.genfromtxt(prefix+'output_nsfd_adaptive_cfl_02/statistics', skip_header=skip, usecols=(1,15))[::10]
nsfd_adaptive_05 = np.genfromtxt(prefix+'output_nsfd_adaptive_cfl_05/statistics', skip_header=skip, usecols=(1,15))[::10]
theta_10_cfl_02 = np.genfromtxt(prefix+'output_theta_10_cfl_02/statistics', skip_header=skip, usecols=(1,15))[::10]

#NSFD results have some superfluous zeros during mesh refinement
nsfd_adaptive_02 = np.array( [ line for line in nsfd_adaptive_02 if line[0] != 0.] )
nsfd_adaptive_05 = np.array( [ line for line in nsfd_adaptive_05 if line[0] != 0.] )

#Read in the relaxation time as computed with power iteration
relaxation_times = []
time = 0.
with open(prefix+'output_nsfd_adaptive_cfl_02/log.txt') as f:
  for l in f.readlines():
    if '*** Timestep' in l:
        time = float(l.split()[3][2:])/1.e6
    if 'New relaxation' in l:
        timescale = float(l.split()[4])/1000.
        relaxation_times.append( [time, timescale] )
relaxation_times = np.array(relaxation_times[3:])

#Plot rayleigh taylor results
plt.figure(figsize=(4,4) )

plt.subplot(111)

marker = itertools.cycle( ('h', 'v', '^', '*', 'D', 's', 'o') )
plt.plot( forward_euler[:,0]/1.e6, -forward_euler[:,1]/1.e3, label='FE dt = 500 yr' )
plt.plot( nsfd_adaptive_02[:,0]/1.e6, -nsfd_adaptive_02[:,1]/1.e3, marker.next(), markevery=0.03, label=r'NSFD CFL=0.2')
plt.plot( nsfd_adaptive_05[:,0]/1.e6, -nsfd_adaptive_05[:,1]/1.e3, marker.next(), markevery=0.03, label=r'NSFD CFL=0.5')
plt.plot( theta_10_cfl_02[:,0]/1.e6, -theta_10_cfl_02[:,1]/1.e3, marker.next(), markevery=0.02, label=r'QI $\theta$=1.0 CFL=0.2')
plt.legend(loc='lower left', prop={'size':10})

plt.xlim(0.,6.)
plt.xlabel('Time (Myr)')
plt.ylabel('Maximum interface depth (km)')

#plt.show()
plt.savefig('rayleigh_taylor.pdf')
plt.clf()

#Load in data for testing the effect of different tau choices
nsfd_static = np.genfromtxt(prefix+'output_nsfd_static/statistics', skip_header=50, usecols=(1,15))
nsfd_static_aggressive = np.genfromtxt(prefix+'output_nsfd_static_aggressive/statistics', skip_header=50, usecols=(1,15))
nsfd_static_loose = np.genfromtxt(prefix+'output_nsfd_static_loose/statistics', skip_header=50, usecols=(1,15))
nsfd_static = np.array( [ line for line in nsfd_static if line[0] != 0.] )
nsfd_static_aggressive = np.array( [ line for line in nsfd_static_aggressive if line[0] != 0.] )
nsfd_static_loose = np.array( [ line for line in nsfd_static_loose if line[0] != 0.] )

plt.figure(figsize=(8,4) )

#Plot RT results
plt.subplot(121)

marker = itertools.cycle( ('h', 'v', '^', '*', 'D', 's', 'o') )
#plt.plot( forward_euler[:,0]/1.e6, -forward_euler[:,1]/1.e3, label='FE dt = 500 yr' )
plt.plot( nsfd_adaptive_02[:,0]/1.e6, -nsfd_adaptive_02[:,1]/1.e3, label=r'NSFD $\tau^* = \tau_\mathrm{min}$')
plt.plot( nsfd_static[:,0]/1.e6, -nsfd_static[:,1]/1.e3, marker.next(), markevery=0.04, label=r'NSFD $\tau^*$ = 1.991 kyr')
plt.plot( nsfd_static_aggressive[:,0]/1.e6, -nsfd_static_aggressive[:,1]/1.e3, marker.next(), markevery=0.04, label=r'NSFD $\tau^*$ = 1 kyr')
plt.plot( nsfd_static_loose[:,0]/1.e6, -nsfd_static_loose[:,1]/1.e3, marker.next(), markevery=0.04, label=r'NSFD $\tau^*$ = 4 kyr')
plt.legend(loc='lower left', prop={'size':10})

plt.title('(a)')
plt.xlim(0.,6.)
plt.xlabel('Time (Myr)')

#Plot relaxation tau with time
plt.subplot(122)

marker = itertools.cycle( ('h-', 'v-', '^-', '*-', 'D-', 's-', 'o-') )
time = np.linspace(0.,6.,1000)
plt.plot( relaxation_times[:,0], relaxation_times[:,1])
plt.plot( time, np.ones_like(time)*1.991, marker.next(), markevery=0.03)
plt.plot( time, np.ones_like(time)*1., marker.next(), markevery=0.03)
plt.plot( time, np.ones_like(time)*4., marker.next(), markevery=0.03)

plt.xlim(0.,6.)
plt.ylim(0.,5.)
plt.xlabel('Time (Myr)')
plt.ylabel(r'$\tau_\mathrm{min}$ (kyr)')
plt.title('(b)')

#plt.show()
plt.savefig('rayleigh_taylor_tau_choice.pdf')
