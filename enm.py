#!/bin/env python

import numpy as np
import sys

cord = np.loadtxt('input.pdb', usecols=(6, 7, 8))
#SS = np.loadtxt('ss.dat', int)

len_ca = len(cord)

# compute squre distane between residues
sqrdist_matrix = np.zeros((len_ca,len_ca),float)
for i in np.arange(len_ca):
	for j in np.arange(i+1,len_ca):			
		dist = cord[i,:] - cord[j,:]
		sqrdist_matrix[i][j] = np.dot(dist,dist)
		sqrdist_matrix[j][i] = sqrdist_matrix[i][j]


# compute (full) connectivity matrix, one connection per pair
print "ENM distance cutoff used: 15 Angstrom"
cutoff = 15.0
sqrcutoff = cutoff*cutoff
conn_matrix = np.empty((len_ca,len_ca),int)
for i in range(len_ca):
	for j in range(i+1):
		conn_matrix[i][j] = 0
	for j in range(i+1,len_ca):
		if (sqrdist_matrix[i][j] <= sqrcutoff):
			conn_matrix[i][j] = 1
		else:
			conn_matrix[i][j] = 0

# connectivity matrix for disulfide linkage 
#for i,j in SS:
#	conn_matrix[i][j] = 10
#	conn_matrix[j][i] = 10

# compute (full) Hessian matrix
print "Now computing Hessian matrix elements..."
hess_matrix = np.zeros((3*len_ca,3*len_ca),float)
# off-diagonal
for i in range(len_ca):
	for j in range (len_ca):
            r = cord[i,:] - cord[j,:]
            if (i==j):
                rsqu = 1
            else:
                rsqu = sqrdist_matrix[i][j]
            for m in range(3):
                for n in range(3):
                    hess_matrix[3*i+m][3*j+n] = -1.0 * (conn_matrix[i][j]+conn_matrix[j][i]) * r[m] * r[n] / rsqu;

# on-diagonal
for i in range(len_ca):
	for j in range(len_ca):
            r = cord[i,:] - cord[j,:]
            if (i==j):
                rsqu = 1
            else:
                rsqu = sqrdist_matrix[i][j]
            for m in range(3):
                for n in range(3):
                    hess_matrix[3*i+m][3*i+n] += (conn_matrix[i][j]+conn_matrix[j][i]) * r[m] * r[n] / rsqu;
                      
# diagonalize Hessian
print "Now diagonalizing Hessian..."
eval,evec = np.linalg.eigh(hess_matrix,"L")

#eigvecs = np.transpose(evec_trans)

# dump modes to pickle
np.savetxt('modes.txt', evec)

# dump frequencies to pickle
np.savetxt('evalues.txt', eval)

