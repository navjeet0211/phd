from prody import *
import matplotlib.pyplot as plt
from pylab import *
import numpy as np

rcParams['figure.figsize'] = 6, 5


# definitions for the axes 
left, width = 0.10, 0.85
bottom, hight = 0.11, 0.8

ax = axes([left, bottom, width, hight])

pca = loadModel('hsa_xray.pca.npz')

anm = loadModel('ed-enm.anm.npz')

overlap = abs(calcOverlap(pca[:7], anm[:7]))
plt.pcolor(overlap, cmap=plt.cm.jet)
plt.colorbar()
x_range = np.arange(1, 8)
plt.xticks(x_range-0.5, x_range)
plt.xlabel('edENM mode index')
y_range = np.arange(1, 8)
plt.yticks(y_range-0.5, y_range)
plt.ylabel('PCA mode index')
plt.axis([0, 7, 0, 7])

#plt.savefig("pca-enm-overlap.eps",dpi=300, papertype='letter', format='eps')
plt.savefig("pca-enm-overlap.png")
#plt.show()
