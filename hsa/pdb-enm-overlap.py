from prody import *
import numpy as np
import matplotlib.pyplot as plt

f = open('pdb-list.dat', 'a')
anm = loadModel('ed-enm.anm.npz')
pca = loadModel('hsa_xray.pca.npz')
ensemble = loadEnsemble('hsa.ens.npz')

I = np.zeros((20,84))
for i in range(1,84):
	f.write(ensemble.getLabels()[i][:4]+'\n')
	for k in range(20):
		Rab = ensemble.getCoordsets()[0]-ensemble.getCoordsets()[i]
		Rab = Rab.reshape(1713,)
		Rab2 = np.dot(Rab,Rab)
		I[k][i-1] = np.dot(Rab, anm.getEigvecs()[:,k])/(np.sqrt(Rab2*np.sqrt(np.dot(anm.getEigvecs()[:,k],anm.getEigvecs()[:,k]))))

np.savetxt('PDB-MODE-overlap.dat', abs(I), fmt=('%.3f'))
