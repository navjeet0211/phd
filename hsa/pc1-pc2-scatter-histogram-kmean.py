import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from prody import *
from pylab import *
from scipy.cluster.vq import *

pca = loadModel('hsa_xray.pca.npz')
ensemble = loadEnsemble('hsa.ens.npz')

# x for pc1 and y for pc2
x = calcProjection(ensemble, pca[:2])[:,0]
y = calcProjection(ensemble, pca[:2])[:,1]

################## k mean data #################
m = x.reshape(-1,1)
n = y.reshape(-1,1)
mn = np.hstack((m,n))
cl = kmeans2(mn, 2)
################################################

nullfmt   = NullFormatter()    # no labels

# definitions for the axes 
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
bottom_h = left_h = left+width+0.02

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom_h, width, 0.2]
rect_histy = [left_h, bottom, 0.2, height]

# start with a rectangular Figure
plt.figure(1, figsize=(8,8))

axScatter = plt.axes(rect_scatter)
axHistx = plt.axes(rect_histx)
axHisty = plt.axes(rect_histy)

# no labels
axHistx.xaxis.set_major_formatter(nullfmt)
axHisty.yaxis.set_major_formatter(nullfmt)

# the scatter plot:
#axScatter.scatter(x, y)
#### plot k mean datat ##########
axScatter.scatter(mn[:,0], mn[:,1], c=cl[1], cmap = plt.cm.jet, facecolor='none')

# now determine nice limits by hand:
binwidth = 0.1
xymax = np.max( [np.max(np.fabs(x)), np.max(np.fabs(y))] )
lim = ( int(xymax/binwidth) + 1) * binwidth

#axScatter.set_xlim( (-lim, 3.5) )
#axScatter.set_ylim( (-2.5, 1) )

axScatter.set_xlabel('PC1', fontsize=14)
axScatter.set_ylabel('PC2', fontsize=14)

bins = np.arange(-lim, lim + binwidth, binwidth)
axHistx.hist(x, bins=bins)
axHisty.hist(y, bins=bins, orientation='horizontal')

axHistx.set_xlim( axScatter.get_xlim() )
axHisty.set_ylim( axScatter.get_ylim() )

plt.savefig("pc1-pc2-proj-kmean.png",dpi=92, papertype='letter', format='png')
plt.show()
