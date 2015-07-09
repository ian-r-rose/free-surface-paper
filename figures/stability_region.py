import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ian')
plt.figure(figsize=(8,4) )

x_nsfd = np.linspace(1.e-10,5, 1000.)
y_nsfd = np.piecewise( x_nsfd , [x_nsfd <= 2., x_nsfd > 2.], [lambda x : 1.e6, lambda x : -x*np.log(1.-2./x)] )
x_kmm = np.linspace(1.e-10,1.-1.e-10, 1000.)
y_kmm = 2./(1.-x_kmm)
y_fe = np.ones_like(x_nsfd)*2.

plt.subplot(121)
plt.xlim(0.,5.)
plt.ylim(0.,10.)
plt.xlabel(r'$\tau^*/\tau_{\mathrm{min}}$')
plt.ylabel(r'$\frac{\Delta t}{\tau_{\mathrm{min}}}$', rotation=0)
plt.fill_between(x_nsfd, 0, y_nsfd, color='green', alpha=0.2)
plt.fill_between(x_nsfd, 0, y_fe, color='blue', alpha=0.2)
plt.title('Non-standard FD')
plt.subplot(122)
plt.xlim(0.,1.)
plt.ylim(0.,10.)
plt.xlabel(r'$\theta$')
plt.fill_between(x_kmm, 0, y_kmm, color='green', alpha=0.2)
plt.fill_between(x_nsfd, 0, y_fe, color='blue', alpha=0.2)
plt.title('Quasi-implicit')
#plt.show()
plt.savefig('stability.pdf')
