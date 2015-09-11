#!/bin/bash

#########################################################
# Author: Navjeet Ahalawat
# Date  : 25 Nov, 2014
#
# Usage: bash checkg09.sh "you_queue_jobname"
#
# example: bash checkg09.sh job_xyz
# 
##########################################################

#!/bin/bash

for node in $(qstat -n1 | grep $1 | awk '{print $12}' | sed 's/\/0\*16+/ /g' | sed 's/\/0\*16/ /')
do

echo "checking node: "$node
ssh $node bash <<'FILE'
#!/bin/bash
# top -b n1 | grep l*.exel
top -b n1 | grep "a.out"
FILE

done

