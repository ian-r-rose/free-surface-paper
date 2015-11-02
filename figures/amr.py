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

plt.figure(figsize=(4,4) )


data_uniform_qi = np.loadtxt("../benchmarks/amr/uniform_qi/resolution_convergence_uniform_qi.txt")
data_uniform_nsfd = np.loadtxt("../benchmarks/amr/uniform_nsfd/resolution_convergence_uniform_nsfd.txt")
data_adaptive_qi = np.loadtxt("../benchmarks/amr/adaptive_qi/resolution_convergence_adaptive_qi.txt")
data_adaptive_nsfd = np.loadtxt("../benchmarks/amr/adaptive_nsfd/resolution_convergence_adaptive_nsfd.txt")

refinement_levels = np.linspace(4., 8., 5)
h_value  =  (2.)**(-refinement_levels)[:-1]

topography_at_3Ma = 397.6

# Get the error, less the point at the highest refinement level,
# where the convergence sort of falls apart, presumably due to
# loss of accuracy due to something else in the solution.
error_uniform_qi = np.abs(data_uniform_qi[:,1] - topography_at_3Ma)[:-1]
error_uniform_nsfd = np.abs(data_uniform_nsfd[:,1] - topography_at_3Ma)[:-1]
error_adaptive_qi = np.abs(data_adaptive_qi[:,1] - topography_at_3Ma)[:-1]
error_adaptive_nsfd = np.abs(data_adaptive_nsfd[:,1] - topography_at_3Ma)[:-1]

# Normalize the errors
error_uniform_qi /= topography_at_3Ma
error_uniform_nsfd /= topography_at_3Ma
error_adaptive_qi /= topography_at_3Ma
error_adaptive_nsfd /= topography_at_3Ma

# Read from console outputs rather than parsing... oh well.
dofs_uniform_qi = np.array([24600, 96296,381000,1515656, 6045960])[:-1] 
dofs_uniform_nsfd = dofs_uniform_qi
dofs_adaptive_qi = np.array([10916, 22994, 55476, 122008, 255296])[:-1]
dofs_adaptive_nsfd = dofs_adaptive_qi


font_size = 12

plt.subplot(111)

marker = itertools.cycle( ('-h', '-v', '-^', '-s') )
plt.loglog(dofs_uniform_qi, error_uniform_qi, marker.next(), markersize=8, label=r'Uniform, QI')
plt.loglog(dofs_uniform_nsfd, error_uniform_nsfd, marker.next(), markersize=8, label=r'Uniform, NSFD')
plt.loglog(dofs_adaptive_qi, error_uniform_qi, marker.next(), markersize=8, label=r'Adaptive, QI')
plt.loglog(dofs_adaptive_nsfd, error_uniform_nsfd, marker.next(), markersize=8, label=r'Adaptive, NSFD')

plt.ylim(1.e-3, 0.3)
plt.xlim(1.e4, 3.e6)
plt.xlabel(r'DoFs')
plt.ylabel(r'Relative topography error')
plt.legend(loc='upper right', fontsize=8)

#plt.show()
plt.savefig('amr.pdf')

