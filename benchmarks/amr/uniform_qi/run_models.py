import os
import numpy as np

def generate_prm( refine ):
  prmfile = open("../crameri_benchmark_2.prm", "r")
  outfile = open("tmp.prm", "w")
  for l in prmfile.readlines():
    if 'Initial global refinement' in l:
      outfile.write('  set Initial global refinement = %i\n'%(refine) )
    elif 'Initial adaptive refinement' in l:
      outfile.write('  set Initial adaptive refinement = %i\n'%(0) )
    elif 'Free surface stabilization theta' in l:
      outfile.write('  set Free surface stabilization theta = 0.5\n')
    elif 'Relaxation time' in l:
      outfile.write('  set Relaxation time = 0.\n')
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

outputfile = open('resolution_convergence_uniform_qi.txt', 'w')
refine = range(4,9)
for r in refine:
  print "Running uniform mesh with %i refinements\n"%(r)
  generate_prm(r)
  os.system('mpirun -n 4 ../../../aspect/build/aspect tmp.prm')
  outputfile.write("%i %f \n" % (r, grab_topography()) )
  outputfile.flush()

outputfile.close()
