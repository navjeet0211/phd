#!/bin/python

import MDAnalysis
from MDAnalysis import *
import warnings

warnings.filterwarnings('ignore')

u = MDAnalysis.Universe("ref.pdb", "amd-all.dcd")
#u = MDAnalysis.Universe("rab.gro", "test.xtc")
atoms1 = u.selectAtoms("resid 236 and name N") + u.selectAtoms("resid 236 and name CA") + u.selectAtoms("resid 236 and name CB") + u.selectAtoms("resid 236 and name CG")
atoms2 = u.selectAtoms("resid 236 and name CA") + u.selectAtoms("resid 236 and name CB") + u.selectAtoms("resid 236 and name CG") + u.selectAtoms("resid 236 and name CD1")

fp = open("chi1-chi2.dat","w")
for ts in u.trajectory:
	chi1 = atoms1.dihedral()
        chi2 = atoms2.dihedral()
	fp.write("%s    %s    %s\n" % (str(ts.frame), str(chi1), str(chi2)))
#	print diheral
fp.close()

