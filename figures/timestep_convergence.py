import matplotlib.pyplot as plt
import numpy as np
import numpy.ma
import itertools

try:
  plt.style.use('ian')
except AttributeError:
  print "old matplotlib version?"
except ValueError:
  print "Cannot find the requested stylesheet"

plt.figure(figsize=(8,8) )

data = np.loadtxt("../benchmarks/timestep_convergence/timestep_convergence.txt")
relaxation_times = set( data[:,0])
relaxation_times = list( relaxation_times)
relaxation_times.sort()


vals = []
for r in relaxation_times:
  tsteps = np.ma.masked_where( data[:,0] != r, data[:,1])
  errors = np.ma.masked_where( data[:,0] != r, data[:,2])
  vals.append( (tsteps, errors ) )

marker = itertools.cycle( ('-h', '-v', '-^', '-*', '-D', '-s', '-o') )
for r, val in zip(relaxation_times, vals):
  plt.loglog(val[0], val[1], marker.next(), markersize=8, label=r'$\tau^* = %0.1f \; \tau_\mathrm{min}$'%(r))

#plot a slope-1 line to guide the eye
x = np.logspace(-1.5, -0.5, 10)
y = 1.e-2*x
plt.loglog(x,y, 'k--')
plt.text(0.1, 0.0005, r'$O(\Delta t)$', fontsize=18)

plt.xlabel(r'$\Delta t / \tau_\mathrm{min}$')
plt.ylabel(r'Error')
plt.legend(loc='lower right')
#plt.show()
plt.savefig('timestep_convergence.pdf')

