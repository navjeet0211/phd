#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

phi = np.loadtxt("phi.dat")
theta = phi - 60

def calc_jcoupling_orig(theta):
    "To calculate 3J-HNHA with original equation"
    j = 7.09*np.cos(np.radians(theta))*np.cos(np.radians(theta)) - 1.42*np.cos(np.radians(theta)) + 1.55
    return np.average(j,0), np.std(j,0)


def calc_jcoupling_Teresa(theta):
    "To calculate 3J-HNHA with Head-Gordon parameters in equation"
    j = 6.51*np.cos(np.radians(theta))*np.cos(np.radians(theta)) - 1.76*np.cos(np.radians(theta)) + 1.60
    return np.average(j,0), np.std(j,0)

def calc_jcoupling_bax15(theta):
    "To calculate 3J-HNHA with Bax new parameters in equation"
    j = 8.83*np.cos(np.radians(theta))*np.cos(np.radians(theta)) - 1.29*np.cos(np.radians(theta)) + 0.20
    return np.average(j,0), np.std(j,0)

jhnha_orig, std_orig = calc_jcoupling_orig(theta)
jhnha_orig = jhnha_orig.reshape(-1,1)
std_orig = std_orig.reshape(-1,1)

jhnha_teresa, std_teresa = calc_jcoupling_Teresa(theta)
jhnha_teresa = jhnha_teresa.reshape(-1,1)
std_teresa = std_teresa.reshape(-1,1)

jhnha_bax, std_bax = calc_jcoupling_bax15(theta)
jhnha_bax = jhnha_bax.reshape(-1,1)
std_bax = std_bax.reshape(-1,1)

np.savetxt("J-coupling-orig.txt", np.hstack((jhnha_orig, std_orig)), fmt='%.4f %.4f')
np.savetxt("J-coupling-teresa.txt", np.hstack((jhnha_teresa, std_teresa)), fmt='%.4f %.4f')
np.savetxt("J-coupling-bax-jacs.txt", np.hstack((jhnha_bax, std_bax)), fmt='%.4f %.4f')

plt.plot(jhnha_orig)
plt.plot(jhnha_teresa)
plt.plot(jhnha_bax)
plt.show()
