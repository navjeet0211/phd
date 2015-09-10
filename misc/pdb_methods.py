"""implement class and methods for handling pdb file"""
import sys
class pdb_struct:
    def __init__(self):
        """create some placeholders for coords, radius, atom name, atom type etc"""
        self.coords = []
        self.radius = []
        self.name = []
        self.element = []
    def readfile(self,pdb_name):
        try:
            pdb_file = file(pdb_name,"r")
            print 'opening file'
        except:
            # print "can't find file", pdb_name
            sys.exit("can't find file")
        contents = pdb_file.readlines()
        pdb_file.close()
        print type(contents)
        print 'lines read: ', len(contents)
        self.natom = 0
        xyz = [float(0.),float(0.),float(0.)]
        # print xyz
        atom_rads = {'C':1.8,'S':1.9,'O':1.6,'N':1.4,'P':1.8,'H':1.0}
        for entry in contents:
            if (entry[0:6] == 'ATOM  ') or (entry[0:6] == 'HETATM'):
                self.natom +=1
                # print entry[:-1]
                xyz[0] = float(entry[30:38])
                xyz[1] = float(entry[38:46])
                xyz[2] = float(entry[46:54])
                self.coords.append([xyz[0],xyz[1],xyz[2]])
                atype = entry[13]
                self.element.append(atype)
                if ( atom_rads.has_key(atype)):
                    self.radius.append(atom_rads[atype])
                else:
                    print "atom radius not in dictionary", atype
                    selfradius.append(0.0)
