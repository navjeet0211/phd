import numpy as np
import matplotlib.pyplot as plt
from pylab import *

rcParams['figure.figsize'] = 6, 5
f = np.loadtxt('1e7e.dat')
#f = np.loadtxt('2bxd.dat')
y = np.sqrt(np.power(f,2).cumsum())

xlim(0.5, 20.5)
ylim(0.0, 1.05)

xticks(np.linspace(1, 20, 20, endpoint=True))
yticks(np.arange(0.0, 1.1, 0.1))

xlabel('ed-ENM mode index')
ylabel('Overlap of modes with conformational change')

x = np.arange(1.0,21.0)
#plot(x,f, 'bo')
lft = np.arange(0.5, 20.5)
bar(lft, f, width=0.8)
plot(x, y, 'go-', label="Cumulative Overlap")
legend(loc=2)
plt.savefig("1e7e_HSA_FA.png")
show()
