#!/usr/bin/perl -w
use Cwd; 
 
#
# How many shifts we will be collecting ?
#
 
(`echo 1 | /opt/apps/gromacs/4.6.4/intel/bin/trjconv_mpi -f ../300.xtc -s ../topol.tpr -pbc mol -ur compact -dump 0 -o frame.pdb`) or die "trajconv made a boo-boo. Too bad ...\n";
`sparta+ -in frame.pdb >& /dev/null`;
`/bin/rm -rf frame.pdb`;
 
open ( IN, "pred.tab" ) or die "Can not open pred.tab. Usage: calc_shifts <dcd> <psf>\n";
while ( $line = <IN> )
  {
    if ( $line =~ /^FORMAT/ )
      {
        last;
      }
  }
 
$line = <IN>;
$tot = 0;
while ( $line = <IN> )
  {
    $ids[ $tot ] = substr( $line, 0, 14 );
    $tot++;
  }
 
close( IN );
 
`/bin/rm -rf *.tab`;
 
if ( $tot < 1 )
  {
    print "Too few atoms for calculating shifts. Something is wrong. Bye.\n";
    exit;
  }
 
 
print "Will be collecting data for $tot atoms. Starting ...\n";

print "Now processing set starting at frame          ";
 
#printf("HHHHHHHH%8d", $first );     # These H's are backspaces ...
 
chdir "/home1/sarora/sarora/sparta_results/charmm36/300";

`echo 1 | /opt/apps/gromacs/4.6.4/intel/bin/trjconv_mpi -s ../topol.tpr -f ../300.xtc -o frame.pdb -pbc mol -ur compact -sep -skip 10`;
 
`sparta+ -in frame*.pdb >& /dev/null`;

chdir "/home1/sarora/sarora/sparta_results/charmm36/sparta";
#`/bin/rm -rf frame*.pdb *_struct.tab`;

 
@files = glob("../300/frame*_pred.tab");
#@files = glob("*.tab");
 
if ( @files == 0 )
  {
    last;
  }
 
foreach $file ( @files )
{
 
`tail -$tot $file | awk '{printf "%8.3f ", \$5}' >> 300_SHIFTS`;
`echo >> 300_SHIFTS`;
}
 
#`/bin/rm -rf frame*.tab`;

print "\n\n";
 
#
# Calculate means + sigmas
#

open ( IN, "300_SHIFTS" ) or die "Can not open SHIFTS ??? How did this happen ???\n";
open (OUT, ">300_FINAL-SHIFTS") or die "Can not open output file for shifts ???\n";
 
for ( $i=0 ; $i < $tot ; $i++ )
{
	$mean= 0.0;
	$nof_lines = 0;
	$std = 0.0;
	while ( $line = <IN> )
	  {
	    @data = split( ' ', $line );
 
	    $nof_lines++;
	    $delta = $data[ $i ] - $mean;
	    $mean += $delta / $nof_lines;
	    $std += $delta * ($data[ $i ] - $mean);
	  }
 
        printf OUT "%s    %8.4f %8.4f\n", $ids[ $i ], $mean, sqrt( $std / ($nof_lines -1));
        seek( IN, 0, 0 );        
}
 
close( IN );
close( OUT );

print "\nAll done.\n\n";

