import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid.axislines import Subplot
from pylab import *
from prody import *

#rcParams['figure.figsize'] = 10, 4
close('all')

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

anm = loadModel('ed-enm.anm.npz')

p = np.array([27, 30, 32, 108, 112, 114, 157, 183, 191, 195, 199, 204, 
				206, 209, 211, 221, 222, 242, 247, 292, 348, 354, 418,
				428, 436, 452, 463, 519, 520, 521, 525, 534])

m = np.array([ 146, 149, 150, 209, 218, 222, 242, 257, 291, 348, 354, 402, 410,  411, 485, 525])

#n = np.array([ 384, 430, 458, 470, 482, 500, 528])
n = np.array([178, 286, 356, 374, 384, 430, 458, 470, 475, 482, 500, 516])

######################################################################
#
#           Calculate sqflucation
#
######################################################################

x = np.arange(5, 576)
y = calcSqFlucts(anm[:8])        # for slow modes
y = y - np.min(y)
y = y/np.max(y)
y1 = calcSqFlucts(anm[-30:])     # for fast modes

#grid()
#xlim(5.0, 575.0)

#xticks(np.array([100, 200, 300, 400, 500, 600]))
#xlabel('Residue index')
#ylabel('Square fluctuations ( $\AA^2$ )')
#ax1 = plt.subplot(211)

ax1.plot(x, y)
ax1.plot(p, y[p-5], 'ro')
ax1.plot(m, y[m-5], 'g^')
ax1.plot(n, y[n-5],  color='y', marker='*', linestyle='none', markersize=8)
ax1.set_yticks([])

ax1.arrow(195, 0.2, 0.0, -0.10, fc="k", ec="k", head_width=5, head_length=0.05)
ax1.arrow(199, 0.2, 0.0, -0.10, fc="k", ec="k", head_width=5, head_length=0.05)
ax1.arrow(352, 0.22, 0.0, -0.10, fc="k", ec="k", head_width=5, head_length=0.05)
ax1.arrow(428, 0.2, 0.0, -0.10, fc="k", ec="k", head_width=5, head_length=0.05)
ax1.arrow(454, 0.2, 0.0, -0.10, fc="k", ec="k", head_width=5, head_length=0.05)
'''
ax1.annotate("",
            xy=(351, 0.07), xycoords='data',
            xytext=(340, 0.3), textcoords='data',color='black',size=7,
            arrowprops=dict(arrowstyle="simple", fc="k", ec="k", 
			connectionstyle="arc3")
             )
'''
#xticks[-1].label1.set_visible(False)
#show()

#ax2 = plt.subplot(212)

ax2.plot(x, y1)
ax2.plot(p, y1[p-5], 'ro')
ax2.plot(m, y1[m-5], 'g^')
#plot(n, y1[n-5], color='#FF00FF', marker='*')

#xticks(np.array([100, 200, 300, 400, 500, 600]))
xlabel('Residue index')
ylabel('Square fluctuations')
frame1 = plt.gca()
frame1.axes.get_yaxis().set_ticks([])

show()

#savefig("sqf-critical_res.png")
