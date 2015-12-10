import matplotlib.pyplot as plt
import numpy as np

try:
  plt.style.use('./free_surface_paper.mplstyle')
except AttributeError:
  print "old matplotlib version?"
except ValueError:
  print "Cannot find the requested stylesheet"

plt.figure(figsize=(8,4) )

ymax = 10. #top of figure

x_nsfd = np.linspace(1.e-10,5, 1000.)
y_nsfd = np.piecewise( x_nsfd , [x_nsfd <= 2., x_nsfd > 2.], [lambda x : ymax, lambda x : -x*np.log(1.-2./x)] )
x_kmm = np.linspace(1.e-10,1.-1.e-10, 1000.)
y_kmm = np.piecewise( x_kmm, [x_kmm <= 0.85, x_kmm > 0.85], [ lambda x :2./(1.-x), lambda x : ymax] )
y_fe = np.ones_like(x_nsfd)*2.

fontsize = 16
plt.subplot(121)
plt.xlim(0.,5.)
plt.ylim(0.,ymax)
plt.xlabel(r'$\tau^*/\tau_{\mathrm{min}}$', fontsize=fontsize)
plt.ylabel(r'$\frac{\Delta t}{\tau_{\mathrm{min}}}$', rotation=0, fontsize=fontsize)
plt.fill_between(x_nsfd, 0, y_nsfd, color='green', alpha=0.2)
plt.fill_between(x_nsfd, 0, y_fe, color='blue', alpha=0.2)
plt.text(0.5, 3., r'Stable', fontsize=fontsize)
plt.text(3., 6., r'Unstable', fontsize=fontsize)
plt.title('(a) Non-standard FD', fontsize=fontsize)
plt.subplot(122)
plt.xlim(0.,1.)
plt.ylim(0.,ymax)
plt.xlabel(r'$\theta$', fontsize=fontsize)
plt.fill_between(x_kmm, 0, y_kmm, color='green', alpha=0.2)
plt.fill_between(x_nsfd, 0, y_fe, color='blue', alpha=0.2)
plt.text(0.7, 3., r'Stable', fontsize=fontsize)
plt.text(0.1, 6., r'Unstable', fontsize=fontsize)
plt.title('(b) Quasi-implicit', fontsize=fontsize)
#plt.show()
plt.savefig('stability_region.pdf')
