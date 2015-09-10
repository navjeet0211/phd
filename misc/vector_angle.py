#!/bin/python

import math
import numpy as np
import MDAnalysis
import warnings
from Bio import PDB

warnings.filterwarnings('ignore')

u = MDAnalysis.Universe("rab.gro", "rab.xtc")
#u = MDAnalysis.Universe("rab.gro", "test.xtc")

fp = open("angle_VectorAB.dat","w")
for ts in u.trajectory:
#	PB = u.selectAtoms("name PB")
#	P1 = PDB.Vector(numpy.array(PB.get_positions(), dtype=float).reshape(3))

        PG = u.selectAtoms("name PG")
        P2 = PG.get_positions().reshape(3)

	O3G = u.selectAtoms("name O3G")
	x3 = O3G.get_positions().reshape(3)

	q78CA = u.selectAtoms("resid 78 and name CA")
	qCA = q78CA.get_positions().reshape(3)

	q78 = u.selectAtoms("resid 78 and name CD")
	qr = q78.get_positions().reshape(3)

#       dist = numpy.linalg.norm(P2 - qr)
#	ppo = math.degrees(PDB.calc_angle(P2, x3, qr))

	a = x3-P2
	b = qr-qCA
	dot = np.dot(a,b)
	x_modulus = np.sqrt((a*a).sum())
	y_modulus = np.sqrt((b*b).sum())
	cos_angle = dot / x_modulus / y_modulus
	angle1 = np.arccos(cos_angle)
	angle = angle1 * 360 / 2 / np.pi
#	print angle
	fp.write("%s		%s\n" % (str(ts.frame), str(angle)))

fp.close()

