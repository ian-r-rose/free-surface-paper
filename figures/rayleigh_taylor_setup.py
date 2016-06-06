import matplotlib.pyplot as plt
import numpy as np

L=500
H=L
thickness=100.

fig = plt.figure( figsize=(8,8) )
ax = fig.add_subplot(111)

ax.axes.get_yaxis().set_major_formatter(plt.NullFormatter())
ax.axes.get_xaxis().set_major_formatter(plt.NullFormatter())
ax.tick_params( top='off', bottom='off', left='off', right='off')

amplitude = 5.0
x = np.linspace(0,L,1000)
interface = -thickness - amplitude*np.cos(2.*np.pi*x/x[-1.])

#plot fluid
ax.plot(x,interface, color='k')
plt.fill_between(x, -L, interface, color='darkgray', alpha=1.0)
plt.fill_between(x, interface, 0., color='dimgray', alpha=1.0)


head_size = 10


#Draw arrow for gravity
ax.arrow(0.3*L, -0.6*L, 0.0, -.15*L, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.2*L,-0.59*L, r'${\bf g}=9.81 \; \mathrm{m}/\mathrm{s}^2$', fontsize=20)

#Add density information
ax.text(0.2*L, -0.10*L, r'$\rho = 3300  \; \mathrm{kg}/\mathrm{m}^3$', fontsize=20)
ax.text(0.2*L, -0.15*L, r'$\eta = 10^{21} \; \mathrm{Pa} \; \mathrm{s}$', fontsize=20)

ax.text(0.2*L, -0.40*L, r'$\rho = 3200  \; \mathrm{kg}/\mathrm{m}^3$', fontsize=20)
ax.text(0.2*L, -0.45*L, r'$\eta = 10^{20} \; \mathrm{Pa} \; \mathrm{s}$', fontsize=20)

#Draw arrow for length
ax.arrow(0.08*L, -0.95*H, 0.85*L, 0.0, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.arrow(0.95*L, -0.95*H, -0.85*L, 0.0, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.5*L, -.94*H, r'$500 \; \mathrm{km}$', fontsize=20)

#Draw arrow for depth
ax.arrow(0.95*L, -0.08*H, 0, -0.83*H, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.arrow(0.95*L, -0.92*H, 0, 0.88*H, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.8*L, -0.5*H, r'$500 \; \mathrm{km}$', fontsize=20)

#Draw arrow for layer thickness
ax.arrow(0.87*L, -0.08*H, 0, -0.09*H, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.arrow(0.87*L, -0.18*H, 0, 0.14*H, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.72*L, -0.12*H, r'$100 \; \mathrm{km}$', fontsize=20)

ax.set_xlim(0,L)
ax.set_ylim(-L,0.)

#plt.show()
plt.savefig("rayleigh_taylor_setup.pdf")
