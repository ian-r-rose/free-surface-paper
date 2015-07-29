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

data = np.loadtxt("../benchmarks/tau_sensitivity/tau_sensitivity.txt")
relaxation_times =  data[:,0]
errors = data[:,2]

plt.semilogy(relaxation_times, errors, '-x', markersize=8)


plt.xlabel(r'$\tau^* / \tau_\mathrm{min}$')
plt.ylabel(r'Error')
#plt.show()
plt.savefig('tau_sensitivity.pdf')

