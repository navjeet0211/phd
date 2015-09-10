#!/usr/bin/env python

import sys
import numpy as np

data = np.loadtxt(sys.argv[1])
N = data.shape[0]

f = data.copy()
f[f<0]+=360
#print N
#print 

def alpha_right(f):
    count_alpha = 0
    for i in range(N):
        if(f[i,0]>200 and f[i,0]<340 and f[i,1]>240 and f[i,1]<360):
                count_alpha += 1
    return count_alpha

def beta_left(f):
    count_beta1 = 0
    for i in range(N):
        if(f[i,0]>180 and f[i,0]<270 and f[i,1]>50 and f[i,1]<240):
                count_beta1 += 1
    return count_beta1

def beta_right(f):
    count_beta1 = 0
    for i in range(N):
        if(f[i,0]>160 and f[i,0]<180 and f[i,1]>110 and f[i,1]<180):
                count_beta1 += 1
    return count_beta1

def PPII(f):
    count_pp = 0
    for i in range(N):
        if(f[i,0]>270 and f[i,0]<340 and f[i,1]>50 and f[i,1]<240):
                count_pp += 1
    return count_pp
    
alpha = alpha_right(f)
beta1 = beta_left(f)
beta2 = beta_right(f)
ppII = PPII(f)

#print N, alpha, beta1, beta2, ppII
print "alpha = ", alpha/float(N)
print "beta = ", (beta1+beta2)/float(N)
print "ppII = ", ppII/float(N)

