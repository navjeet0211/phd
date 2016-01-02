#!/usr/bin/env python
from __future__ import division
import numpy    # for histogram stuff
from numpy import *
import optparse
import os
import glob
from collections import defaultdict
from IPython import parallel
import sys
import scipy
import string
from tables import *
import re
import time
import pickle 
import itertools

"""
This code is designed to calculate the mutual information between the dihedral angles of protein amino acid
Args:
      dir: the directory with the dihedral angles(with extension .xvg). This program is designed to work with the g-chi gromacs utility Please Make sure that the dihedral files are sequentially labelled(1-> total_n_residues)
      total_n_residues: The total number of residues.
      n_iterations: How many items the data needs to be scrambled
      skiprows: The number of rows that need to be skipped in each .xvg file(eg g-chi out put has the first 12 rows as junk data) 
      bin_n: number of bins
Returns:
      Mutual Information
"""

def entropy(counts):
    '''Compute entropy.'''
    ps = counts/float(sum(counts))  # coerce to float and normalize
    ps = ps[nonzero(ps)]            # toss out zeros
    H = -sum(ps * log(ps))   # compute entropy

    return H


def python_mi(x, y, bins):
    '''Compute mutual information'''
    counts_xy = histogram2d( x, y, bins=bins, range=[[-180, 180], [-180, 180]])[0]
    counts_x  = histogram( x, bins=bins, range=[-180, 180])[0]
    counts_y  = histogram( y, bins=bins, range=[-180, 180])[0]

    H_xy = entropy(counts_xy) + (len(nonzero(counts_xy)[0])-1)/(2*float(sum(counts_xy)))
    H_x  = entropy(counts_x) + (len(nonzero(counts_x)[0])-1)/(2*float(sum(counts_x)))
    H_y  = entropy(counts_y) + (len(nonzero(counts_x)[0])-1)/(2*float(sum(counts_y)))

    return H_x + H_y - H_xy


def create_hd5files_from_xvg(dir,skiprows):
    filename_list=glob.glob('%s/*.xvg'%dir)
    for i,filename in enumerate(filename_list):
    #creating hdf5 files for those that have not been created before. 
        if not (os.path.exists(filename+'.h5')):
            h5file=open_file(filename+'.h5',"w",title="time")
            time_dihedral=h5file.create_group("/",'time')
            data=numpy.loadtxt(filename,usecols=(1,),skiprows=skiprows)
            grid=h5file.create_array('/time','grid',data)
            h5file.close()


def mutual_information_from_files(res_name1, res_id1, res_name2, res_id2, dir, skiprows, bin_n):
    #mutual_information_from_files

    import numpy
    import os
    import scipy.special as sps
    import scipy.stats as scipy
    from scipy.stats.stats import pearsonr
    import glob
    from scipy.stats.stats import pearsonr
    
    import tables
    import sys
#    result = {}

            # example file namephiALA1.xvg.all_data_450micro
            #f.root.time_dihedral.grid[1]
    filename_id1 = glob.glob('%s/%s???%d.xvg.h5' %(dir,res_name1,res_id1))
    filename_id2 = glob.glob('%s/%s???%d.xvg.h5' %(dir,res_name2,res_id2))
#    print res_name1, res_name2, res_id1, res_id2, filename_id1, filename_id2
    if  filename_id1 and filename_id2:
        f = tables.open_file(filename_id1[0])
        dihedral_id1 = numpy.array(f.root.time.grid[:])
        f.close()
        
        f = tables.open_file(filename_id2[0])
        dihedral_id2 = numpy.array(f.root.time.grid[:])
	mi = python_mi(dihedral_id1, dihedral_id2, bin_n)
	f.close()
#        result[ res_name1, res_id1, res_name2, res_id2 ] = mi
    return mi


'''
def create_torsions_pairs_number_matrix(total_n_residues):
    # matrix having elements as total number of pairs between two residues
    resfile = open('reslist.dat', 'r')
    reslist = ['ALA',  'CYS', 'ASP', 'GLU', 'PHE', 'GLY', 'HIS', 'ILE', 'LYS', 'LEU', 'MET', 'ASN', 'PRO', 'GLN', 'ARG', 'SER', 'THR', 'VAL', 'TRP', 'TYR']
    ntors = {'ALA': 2, 'ARG': 6, 'ASN': 4, 'ASP': 4, 'CYS': 3, 'GLN': 5, 'GLU': 5, 'GLY': 2, 'HIS': 5, 'ILE': 4, 'LEU': 4, 'LYS': 6, 'MET': 5, 'PHE': 4, 'PRO': 4, 'SER': 3, 'THR': 3, 'TRP': 4, 'TYR': 4, 'VAL': 3}
    pairs = [pair for pair in itertools.product(reslist, reslist)]

    pairs_dict = {}
    for i in xrange(len(pairs)):
        if (pairs[i][0] == pairs[i][1]):
            pairs_dict[pairs[i]] = (ntors[pairs[i][0]]*(ntors[pairs[i][0]]+1))/2
        else:
            pairs_dict[pairs[i]] = ntors[pairs[i][0]]*ntors[pairs[i][1]]

    l = resfile.readlines()
    n_tor_pairs = numpy.zeros((total_n_residues,total_n_residues))
    for i in range(total_n_residues):
        for j in range(total_n_residues):
            n_tor_pairs[i,j] = pairs_dict[l[i].split()[1], l[j].split()[1]]
    numpy.savetxt('n_tor_pairs.txt', n_tor_pairs, fmt='%.2f')

    return n_tor_pairs.astype(float)
'''


def main(dir, total_n_residues, skiprows, bin_n):
    olderr = numpy.seterr(all='ignore')
    #dihedral names
    dihedral_names = ['chi1','chi2','chi3','chi4','phi','psi']
    #dict of results
    results_dict = {}
    for i in xrange(total_n_residues):
        for j in xrange(i,total_n_residues):
            results_dict[i+1,j+1] = []

    results = numpy.zeros((total_n_residues,total_n_residues))
    #time_jump for saving results in seconds

    file_name_list=glob.glob('%s/*.h5'%dir)
    print "Found",len(file_name_list),"files"
    #for all possible files found
    for i,file_id1 in enumerate(file_name_list):
        #extract the name of the dihedral 
	name1=re.findall("chi1|chi2|chi3|chi4|phi|psi",file_name_list[i])[0]
	#extract the id
        id1=int((re.findall("[A-Z]{3}\d+",file_name_list[i])[0])[3:])
        #limit the file_list to what ever is left so that we dont overcount
        for j,file_id2 in enumerate(file_name_list[i:]):
        #get the name and id for the second residue
            name2=re.findall("chi1|chi2|chi3|chi4|phi|psi",file_name_list[i+j])[0]
            id2=int((re.findall("[A-Z]{3}\d+",file_name_list[i+j])[0])[3:])
            mi_output = mutual_information_from_files(name1, id1, name2, id2, dir, skiprows, bin_n)

            if (id1 < id2):
                results_dict.setdefault((id1,id2), []).append(mi_output)
            else:
                results_dict.setdefault((id2,id1), []).append(mi_output)
            # print id1, id2, name1, name2, mi_output

    for i in xrange(total_n_residues):
        for j in xrange(i,total_n_residues):
            if (i==j):
                results[i,j] = sum(results_dict[i+1,j+1])/len(results_dict[i+1,j+1])
            else:
                results[i,j] = sum(results_dict[i+1,j+1])/len(results_dict[i+1,j+1])
                results[j,i] = results[i,j]

    pickle.dump( results_dict, open("bin_35_dihedral_mi.p", "wb") )
    numpy.savetxt("bin_35_dihedral_mi.txt", results, fmt='%.6f')


def parse_commandline():
    import os
    parser = optparse.OptionParser()
    parser.add_option('-d', '--directory', dest='dir',default=os.getcwd(), help='directory with chi1,phi,psi files')
    parser.add_option('-t','--total_residues',dest='t',type="int",help='total number of residues')
    parser.add_option('-s', '--skip_rows', dest='s',type='int', default=12,help='how many rows to skip')
    parser.add_option('-b', '--bins',dest='bin_n', type='int', default=24, help='The number of Bins used to bin data(Default 24). Too few bins can lead to problems')
    (options, args) = parser.parse_args()
    return (options, args)

#function main if namespace is main

if __name__ == "__main__":
    (options, args) = parse_commandline()
    create_hd5files_from_xvg(options.dir,options.s)
    main(dir = options.dir, total_n_residues = options.t, skiprows = options.s, bin_n = options.bin_n)
