#!/usr/bin/python

import sys, getopt
import numpy as np
import matplotlib.pyplot as plt

def plotCorr():
    inputfile = sys.argv[2]
    outputfile = sys.argv[4]
    fi = open(inputfile, 'r')
    #fo = open('corr-matrix.dat', 'w')
    firstline = fi.readline()
    m, n = firstline.split()[0], firstline.split()[2]
    m, n = int(m), int(n)
    corrmat = np.zeros(m*n)
    i = 0
    for line in fi:
        list = line.split()
        for corrval in list:
    	    if (corrval != "]"):
                corrmat[i] = corrval
                i = i+1

    corrmat = corrmat.reshape(m,n)
    '''
    for i in range(578):
	for j in range(578):
	    fo.write("%s %s %s\n" % (i, j, corrmat[i,j]))
    '''
    np.savetxt(outputfile+".dat", corrmat, fmt="%.4f")
    plt.imshow(corrmat,origin='lower')
    plt.colorbar()
    plt.savefig(outputfile+".png")

def main(argv):
    inputfile = ''
    outputfile = ''
    if len(argv) < 3:
        sys.stderr.write("Usage: ./read-blitz.py -i <inputfile> -o <outputfile>\n")
        sys.exit(1)
    try:
        opts, args = getopt.getopt(argv,"hi:o",["ifile=","ofile"])
    except getopt.GetoptError:
        print 'Usage: ./read-blitz.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: ./read-blitz.py -i <inputfile> -o <outputfile>\n'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile

    plotCorr()

if __name__ == "__main__":
   main(sys.argv[1:])

