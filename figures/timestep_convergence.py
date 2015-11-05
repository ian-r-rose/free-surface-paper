import matplotlib.pyplot as plt
import numpy as np
import numpy.ma
import itertools

try:
  plt.style.use('./free_surface_paper.mplstyle')
except AttributeError:
  print "old matplotlib version?"
except ValueError:
  print "Cannot find the requested stylesheet"

plt.figure(figsize=(8,4) )


#Plot convergence of the NSFD scheme

data = np.loadtxt("../benchmarks/timestep_convergence/timestep_convergence.txt")
relaxation_times = set( data[:,0])
relaxation_times = list( relaxation_times)
relaxation_times.sort()


vals = []
for r in relaxation_times:
  # Remove last point, where limit of analytical solution is probably reached
  tsteps = np.ma.compressed(np.ma.masked_where( data[:,0] != r, data[:,1]))[:-1]
  errors = np.ma.compressed(np.ma.masked_where( data[:,0] != r, data[:,2]))[:-1] 
  vals.append( (tsteps, errors ) )

plt.subplot(121)

marker = itertools.cycle( ('-h', '-v', '-^', '-*', '-D', '-s', '-o') )
for r, val in zip(relaxation_times, vals):
  plt.loglog(val[0], val[1], marker.next(), markersize=4, label=r'$\tau^* = %0.1f \; \tau_\mathrm{min}$'%(r))

#plot a slope-1 line to guide the eye
x = np.logspace(-1.5, -0.5, 10)
y = 1.e-2*x
plt.loglog(x,y, 'k--')
plt.text(0.1, 0.0005, r'$O(\Delta t)$', fontsize=9)

plt.xlabel(r'$\Delta t / \tau_\mathrm{min}$')
plt.ylabel(r'Error')
plt.xlim(0.01, 2)
try:
  plt.legend(loc='lower right')
  plt.legend(loc='lower right', fontsize=8)
except:
  pass
plt.title('(a) Non-standard FD')


#Plot convergence of the QI scheme

data = np.loadtxt("../benchmarks/timestep_convergence_qi/timestep_convergence_qi.txt")
thetas = set( data[:,0])
thetas = list( thetas)
thetas.sort()

plt.subplot(122)

vals = []
for theta in thetas:
  # Remove last point, where limit of analytical solution is probably reached
  tsteps = np.ma.compressed(np.ma.masked_where( data[:,0] != theta, data[:,1]))[:-1]
  errors = np.ma.compressed(np.ma.masked_where( data[:,0] != theta, data[:,2]))[:-1]
  vals.append( (tsteps, errors ) )

marker = itertools.cycle( ('-h', '-v', '-^', '-*', '-D', '-s', '-o') )
for theta, val in zip(thetas, vals):
  plt.loglog(val[0], val[1], marker.next(), markersize=4, label=r'$\theta = %0.1f$'%(theta))

#plot a slope-1 and slope-2 lines to guide the eye
x1 = np.logspace(-1.5, -0.5, 10)
x2 = np.logspace(-1.3, -0.3, 10)
y1 = 1.e0*x
y2 = 3.e-2*x*x
plt.loglog(x1,y1, 'k--')
plt.loglog(x2,y2, 'k--')
plt.text(0.1, 0.05, r'$O(\Delta t)$', fontsize=9)
plt.text(0.3, 0.0005, r'$O(\Delta t^2)$', fontsize=9)

plt.xlim(0.01, 2)
plt.xlabel(r'$\Delta t / \tau_\mathrm{min}$')
try:
  plt.legend(loc='lower right')
  plt.legend(loc='lower right', fontsize=8)
except:
  pass

plt.title('(b) Quasi-implicit')



#plt.show()
plt.savefig('timestep_convergence.pdf')

