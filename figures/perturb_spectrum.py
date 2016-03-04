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

plt.figure(figsize=(4,4) )

data = np.loadtxt("../benchmarks/perturb_spectrum/perturb_spectrum.txt")
tsteps =  data[:,0]
thetas = data[:,1]
analytic_times = data[:,2]
numerical_times = data[:,3]

zero_theta = []
zero_tstep = []
mid_theta = []
mid_tstep = []
high_theta = []
high_tstep = []
for tstep, theta, time in zip(tsteps, thetas, numerical_times):
    if theta == 0.0:
        zero_theta.append(time)
        zero_tstep.append(tstep)
    if theta == 0.5:
        mid_theta.append(time)
        mid_tstep.append(tstep)
    if theta == 1.0:
        high_theta.append(time)
        high_tstep.append(tstep)

tau_min = min(analytic_times)

plt.plot(zero_tstep/tau_min, zero_theta/tau_min, 'o', markersize=10, label=r'$\theta=0.0$')
plt.plot(mid_tstep/tau_min, mid_theta/tau_min, 'o', markersize=10, label=r'$\theta=0.5$')
plt.plot(high_tstep/tau_min, high_theta/tau_min, 'o', markersize=10, label=r'$\theta=1.0$')
plt.plot(tsteps/tau_min, analytic_times/tau_min, 'o',markersize=5, c='k', label='analytic')

plt.legend(loc='upper left', numpoints=1)

plt.xlabel(r'$\Delta t/\tau_{\mathrm{min}}$')
plt.ylabel(r'$\tau_s/\tau_{\mathrm{min}}$')
plt.xlim(-0.05, 1.05)
plt.ylim(0.95, 2.05)
#plt.show()
plt.savefig('perturb_spectrum.pdf')

