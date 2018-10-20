import struct
import glob, sys
import numpy as np
from data_import import parse_pfd
import matplotlib.pyplot as plt

pfd_files = glob.glob('/home/psr/visualization_project_sap/pfd/PFFTS_4745_01_0001_pfd/*.pfd')



metadata = [parse_pfd(f) for f in pfd_files]


labelx = sys.argv[1]
labely = sys.argv[2]

x = [f[labelx] for f in metadata]
y = [f[labely] for f in metadata]
plt.scatter(x, y, c = 'k')
plt.xlabel(labelx)
plt.ylabel(labely)
plt.show()



