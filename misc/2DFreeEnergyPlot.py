#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import warnings

warnings.filterwarnings("ignore")

def loadfiletoarray(file):
    data=np.loadtxt(file, usecols=[0,1])
    return data

def assignbins(dim, args):
    minimum=float(dim[0])
    maximum=float(dim[1])
    if args.bw:
        bw=float(args.bw)
    else :
        bw = 5
    bins=np.arange(minimum,(maximum+bw),bw)
    return bins

def prephist(hist2, cb_max):
    hist2=.5961*np.log(hist2) ####Convert to free energy in Kcal/mol
    hist2=np.max(hist2)-hist2  ## zero value to lowest energy state
    ##remove infinity values from free energy plot
    temphist=hist2
    #max value to set infinity values to is cb_max
    for y in range(len(temphist[0,:])):
        for x in range(len(temphist[:,0])):
            if np.isinf(temphist[x,y]):
                temphist[x,y]=cb_max
    return temphist

###########  MAIN  #############
def main():
    args = cmdlineparse()   
    
    inputfile=loadfiletoarray(args.input)
    length=inputfile[:,0]
    
    rows = len(length)

    if args.Xdim:
        binsX= assignbins(args.Xdim, args)
    else:
        binsX= assignbins([-180,180], args)
    if args.Ydim:
        binsY= assignbins(args.Ydim, args)
    else:
        binsY= assignbins([-180,180], args)

    ##HISTOGRAM EVERYTHING
    hist2, edgesX, edgesY = np.histogram2d(inputfile[:,0], inputfile[:,1], bins=(binsX, binsY))
    cb_max=8  ## MAX VALUE TO SET ALL INFINITY VALUES AND TO SET THE COLORBAR TOO
    hist2=prephist(hist2, cb_max)

    cbar_ticks=[0, cb_max*.25, cb_max*.5, cb_max*.75, cb_max]
    plt.figure(1, figsize=(11,8.5))
    extent = [edgesX[0], edgesX[-1], edgesY[-1], edgesY[0]]

    plt.imshow(hist2.transpose(), extent=extent, interpolation='gaussian')
    cb = plt.colorbar(ticks=cbar_ticks, format=('%.1f'))
    imaxes = plt.gca()
    plt.axes(cb.ax)
    plt.clim(vmin=0,vmax=cb_max)
    plt.yticks(fontsize=18)
    plt.axes(imaxes)
    axis=(min(binsX), max(binsX), min(binsY), max(binsY))
    plt.axis(axis)
    plt.xticks(size='18')
    plt.yticks(size='18')
    plt.savefig('2D_Free_energy_surface.png', bbox_inches=0)
    plt.show()

def cmdlineparse():
    parser = ArgumentParser(description="command line arguments")
    parser.add_argument("-input", dest="input", required=True, help="2D input file", metavar="<2D input file>")
    parser.add_argument("-Xdim", dest="Xdim", required=False, nargs="+", help="Xdimensions", metavar="<Xmin Xmax >")
    parser.add_argument("-Ydim", dest="Ydim", required=False, nargs="+", help="Ydimension", metavar="<Ymin Ymax >")
    parser.add_argument("-bw", dest="bw", required=False,  help="Binwidth", metavar="<Binwidth >")
    args=parser.parse_args()
    return args
        
if __name__ == '__main__':
    main()
    
