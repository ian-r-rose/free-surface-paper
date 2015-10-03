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

plt.figure(figsize=(8,4) )


data_uniform_qi = np.loadtxt("../benchmarks/amr/uniform_qi/resolution_convergence_uniform_qi.txt")
data_uniform_nsfd = np.loadtxt("../benchmarks/amr/uniform_nsfd/resolution_convergence_uniform_nsfd.txt")
data_adaptive_qi = np.loadtxt("../benchmarks/amr/adaptive_qi/resolution_convergence_adaptive_qi.txt")
data_adaptive_nsfd = np.loadtxt("../benchmarks/amr/adaptive_nsfd/resolution_convergence_adaptive_nsfd.txt")

refinement_levels = np.linspace(4., 8., 5)
h_value  =  (2.)**(-refinement_levels)

topography_at_3Ma = 397.6

error_uniform_qi = np.abs(data_uniform_qi[:,1] - topography_at_3Ma)
error_uniform_nsfd = np.abs(data_uniform_nsfd[:,1] - topography_at_3Ma)
error_adaptive_qi = np.abs(data_adaptive_qi[:,1] - topography_at_3Ma)
error_adaptive_nsfd = np.abs(data_adaptive_nsfd[:,1] - topography_at_3Ma)


font_size = 12

plt.subplot(121)

marker = itertools.cycle( ('-h', '-v') )
plt.loglog(h_value, error_uniform_qi, marker.next(), markersize=8, label=r'QI')
plt.loglog(h_value, error_uniform_nsfd, marker.next(), markersize=8, label=r'NSFD')

plt.text(1.2e-3,3.e-1, '5.5 MDoF', fontsize = font_size)
plt.text(2.1e-3,1.2e0, '1.4 MDoF', fontsize = font_size)
plt.text(4.e-3,5.e0, '347 kDoF', fontsize = font_size)
plt.text(1.e-2,3.7e1, '88 kDoF', fontsize = font_size)
plt.text(2.e-2,6.5e1, '22 kDoF', fontsize = font_size)

plt.xlabel(r'h')
plt.ylabel(r'Topography error at 3 Ma (m)')
plt.legend(loc='lower right', fontsize=8)
plt.title("Uniform refinement")

plt.subplot(122)

marker = itertools.cycle( ('-h', '-v') )
plt.loglog(h_value, error_adaptive_qi, marker.next(), markersize=8, label=r'QI')
plt.loglog(h_value, error_adaptive_nsfd, marker.next(), markersize=8, label=r'NSFD')
plt.xlabel(r'h')
plt.legend(loc='lower right', fontsize=8)
plt.title("Adaptive refinement")

plt.text(1.2e-3,3.e-1, '233 kDoF', fontsize = font_size)
plt.text(2.1e-3,1.2e0, '111 kDoF', fontsize = font_size)
plt.text(5.e-3,4.e0, '51 kDoF', fontsize = font_size)
plt.text(1.e-2,3.7e1, '21 kDoF', fontsize = font_size)
plt.text(2.e-2,6.5e1, '10 kDoF', fontsize = font_size)

#plt.show()
plt.savefig('amr.pdf')

