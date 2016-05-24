import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure( figsize=(8,8) )
ax = fig.add_subplot(111)

ax.axes.get_yaxis().set_major_formatter(plt.NullFormatter())
ax.axes.get_xaxis().set_major_formatter(plt.NullFormatter())
ax.tick_params( top='off', bottom='off', left='off', right='off')

amplitude = 0.1
x = np.linspace(0,1,1000)
surface = 1.0 + amplitude*np.cos(np.pi*x)
ref_surface = 1.0*np.ones_like(x)

#plot fluid
ax.plot(x,surface, color='k')
ax.plot(x,ref_surface, 'k--')
plt.fill_between(x, 0, surface, color='gray', alpha=0.2)


head_size = 0.02

#Draw arrow for surface perturbation
ax.arrow(0.95, 1.0, 0.0, -0.8*amplitude+head_size, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.9, .95, r'$\zeta_0$', fontsize=20)

#Draw arrow for depth
ax.arrow(0.05, 0.05, 0.0, 0.9, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.arrow(0.05, 0.95, 0.0, -0.9, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.07, .5, r'$D$', fontsize=20)

#Draw arrow for length
ax.arrow(0.08, 0.05, 0.85, 0.0, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.arrow(0.95, 0.05, -0.85, 0.0, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.5, .07, r'$L$', fontsize=20)

#Draw arrow for gravity
ax.arrow(0.8, 0.5, 0.0, -.15, head_width=head_size, head_length=head_size, fc='k', ec='k')
ax.text(0.82,0.43, r'${\bf g}$', fontsize=20)

ax.set_xlim(0,1)
ax.set_ylim(0,1.0 + amplitude)

#plt.show()
plt.savefig("benchmark_setup.pdf")
