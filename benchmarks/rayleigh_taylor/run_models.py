import os
import numpy as np

def generate_prm( output_dir_name, cfl, max_tstep, use_nsfd, relaxation_time, theta ):
  prmfile = open("rayleigh_taylor.prm", "r")
  outfile = open("tmp.prm", "w")
  for l in prmfile.readlines():
    if 'Output directory' in l:
      outfile.write('  set Output directory = %s\n'%(output_dir_name))
    elif 'CFL numer' in l:
      outfile.write('  set CFL number = %f\n'%(cfl) )
    elif 'Maximum time step' in l:
      outfile.write('  set Maximum time step = %f\n'%(max_tstep) )
    elif 'Free surface stabilization theta' in l:
      outfile.write('  set Free surface stabilization theta = %f\n'%(theta))
    elif 'Relaxation time' in l:
      outfile.write('  set Relaxation time = %f\n'%(relaxation_time))
    elif 'Use nonstandard finite difference scheme' in l:
      outfile.write('  set Use nonstandard finite difference scheme = %s\n'%("true" if use_nsfd else "false"))
    else:
      outfile.write(l)
  prmfile.close()
  outfile.close()

models = []
models.append( ('output_nsfd_adaptive_cfl_02', 0.2, 5.e300, True, 0.0, 0.0) )
models.append( ('output_nsfd_adaptive_cfl_05', 0.5, 5.e300, True, 0.0, 0.0) )
#models.append( ('output_nsfd_adaptive_cfl_08', 0.8, 5.e300, True, 0.0, 0.0) )
#models.append( ('output_nsfd_adaptive_small_tstep', 1.0, 500., True, 0.0, 0.0) )

models.append( ('output_nsfd_static', 0.2, 5.e300, True, 1991.0, 0.0) )
models.append( ('output_nsfd_static_aggressive', 0.2, 5.e300, True, 1000.0, 0.0) )
models.append( ('output_nsfd_static_loose', 0.2, 5.e300, True, 4000.0, 0.0) )

#models.append( ('output_theta_05_cfl_02', 0.2, 5.e300, False, 0.0, 0.5) )
models.append( ('output_theta_10_cfl_02', 0.2, 5.e300, False, 0.0, 1.0) )
#models.append( ('output_theta_10_small_tstep', 1.0, 500., False, 0.0, 1.0) )

models.append( ('output_small_time_step', 1.0, 500., False, 0.0, 0.0) )

import os
for m in models:
  if os.path.exists(m[0]+'/statistics') is False or os.path.getmtime(m[0]+'/statistics') < os.path.getmtime('rayleigh_taylor.prm'):
      print "Running model %s\n"%(m[0])
      generate_prm(*m)
      os.system('mpirun -n 4 ../../aspect/build/aspect tmp.prm')
  else:
      print "Skipping model %s\n"%(m[0])
