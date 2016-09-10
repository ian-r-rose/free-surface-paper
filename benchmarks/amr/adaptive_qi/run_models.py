import os
import numpy as np

def generate_prm( refine ):
  prmfile = open("../crameri_benchmark_2.prm", "r")
  outfile = open("tmp.prm", "w")
  for l in prmfile.readlines():
    if 'Initial global refinement' in l:
      outfile.write('  set Initial global refinement = 3\n')
    elif 'Initial adaptive refinement' in l:
      outfile.write('  set Initial adaptive refinement = %i\n'%(refine) )
    elif 'Free surface stabilization theta' in l:
      outfile.write('  set Free surface stabilization theta = 0.5\n')
    elif 'Relaxation time' in l:
      outfile.write('  set Relaxation time = 0.\n')
    elif 'Time steps between mesh refinement' in l:
      outfile.write('  set Time steps between mesh refinement = 10\n')
    elif 'Use nonstandard finite difference scheme' in l:
      outfile.write('  set Use nonstandard finite difference scheme = false\n')
    else:
      outfile.write(l)
  prmfile.close()
  outfile.close()

def grab_topography():
  data = np.genfromtxt("output/statistics", usecols=(1,14))
  time = data[:,0]
  topo = data[:,1]

  topography = topo[ np.argmin( np.abs(time - 3.e6)) ]
  return topography

outputfile = open('resolution_convergence_adaptive_qi.txt', 'w')
refine = range(1,6)
for r in refine:
  print "Running uniform mesh with %i total refinements\n"%(r+3)
  generate_prm(r)
  os.system('mpirun -n 4 ../../../aspect/build/aspect tmp.prm')
  outputfile.write("%i %f \n" % (r, grab_topography()) )
  outputfile.flush()

outputfile.close()
