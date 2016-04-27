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

forward_euler = np.genfromtxt(prefix+'output_small_time_step/statistics', skip_header=50, usecols=(1,15))
nsfd_adaptive_02 = np.genfromtxt(prefix+'output_nsfd_adaptive_cfl_02/statistics', skip_header=50, usecols=(1,15))
nsfd_adaptive_05 = np.genfromtxt(prefix+'output_nsfd_adaptive_cfl_05/statistics', skip_header=50, usecols=(1,15))
theta_10_cfl_02 = np.genfromtxt(prefix+'output_theta_10_cfl_02/statistics', skip_header=50, usecols=(1,15))


nsfd_adaptive_02 = np.array( [ line for line in nsfd_adaptive_02 if line[0] != 0.] )
nsfd_adaptive_05 = np.array( [ line for line in nsfd_adaptive_05 if line[0] != 0.] )

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

plt.figure(figsize=(8,4) )

plt.subplot(121)

marker = itertools.cycle( ('h', 'v', '^', '*', 'D', 's', 'o') )
interval = 100
plt.plot( forward_euler[:,0]/1.e6, -forward_euler[:,1]/1.e3, label='FE dt = 500 yr' )
plt.plot( nsfd_adaptive_02[:,0]/1.e6, -nsfd_adaptive_02[:,1]/1.e3, marker.next(), markevery=int(len(nsfd_adaptive_02[:,0])/interval), label=r'NSFD CFL=0.2')
plt.plot( nsfd_adaptive_05[:,0]/1.e6, -nsfd_adaptive_05[:,1]/1.e3, marker.next(), markevery=int(len(nsfd_adaptive_05[:,0])/interval), label=r'NSFD CFL=0.5')
plt.plot( theta_10_cfl_02[:,0]/1.e6, -theta_10_cfl_02[:,1]/1.e3, marker.next(), markevery=int(len(theta_10_cfl_02[:,0])/interval), label=r'QI $\theta$=1.0 CFL=0.2')
plt.legend(loc='lower left', prop={'size':10})

plt.xlim(0.,6.)
plt.xlabel('Time (Myr)')
plt.ylabel('Maximum interface depth (km)')
plt.title('(a)')

plt.subplot(122)


plt.plot( relaxation_times[:,0], relaxation_times[:,1])
plt.xlim(0.,6.)
plt.ylim(0.,3.)
plt.xlabel('Time (Myr)')
plt.ylabel(r'$\tau_\mathrm{min}$ (kyr)')
plt.title('(b)')

#plt.show()
plt.savefig('rayleigh_taylor.pdf')
