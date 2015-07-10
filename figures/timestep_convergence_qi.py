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

data = np.loadtxt("../benchmarks/timestep_convergence_qi/timestep_convergence_qi.txt")
thetas = set( data[:,0])
thetas = list( thetas)
thetas.sort()


vals = []
for theta in thetas:
  tsteps = np.ma.masked_where( data[:,0] != theta, data[:,1])
  errors = np.ma.masked_where( data[:,0] != theta, data[:,2])
  vals.append( (tsteps, errors ) )

marker = itertools.cycle( ('-h', '-v', '-^', '-*', '-D', '-s', '-o') )
for theta, val in zip(thetas, vals):
  plt.loglog(val[0], val[1], marker.next(), markersize=8, label=r'$\theta = %0.1f$'%(theta))

#plot a slope-1 line to guide the eye
x = np.logspace(-1.5, -0.5, 10)
y = 1.e0*x
plt.loglog(x,y, 'k--')
plt.text(0.1, 0.05, r'$O(\Delta t)$', fontsize=18)

plt.xlabel(r'$\Delta t / \tau_\mathrm{min}$')
plt.ylabel(r'Error')
plt.legend(loc='lower right')
#plt.show()
plt.savefig('timestep_convergence_qi.pdf')

