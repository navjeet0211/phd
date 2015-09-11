#!/bin/bash

total=$(qstat -a | grep -v "Q   --" | grep -v hmq | awk 'NR>5 {sum+=$6}END{print sum}')
short1=$(qstat -a | grep -v "Q   --" | grep "short1" | awk '{sum+=$6}END{print sum}')
short2=$(qstat -a | grep -v "Q   --" | grep "short2" | awk '{sum+=$6}END{print sum}')
medium1=$(qstat -a | grep -v "Q   --" | grep "medium1" | awk '{sum+=$6}END{print sum}')
medium2=$(qstat -a | grep -v "Q   --" | grep "medium2" | awk '{sum+=$6}END{print sum}')
nahlawat=$(qstat -u nahlawat | grep -v "Q   --" | awk '{sum+=$6}END{print sum}')
sdas=$(qstat -u sdas | grep -v "Q   --" | awk '{sum+=$6}END{print sum}')
rasenjit=$(qstat -u rasenjit | grep -v "Q   --" | awk '{sum+=$6}END{print sum}')
rajesh=$(qstat -u rajesh | grep -v "Q   --" | awk '{sum+=$6}END{print sum}')
changdev=$(qstat -u changdev | grep -v "Q   --" | awk '{sum+=$6}END{print sum}')

echo " "
echo "################################################"
echo ""
echo "        Total used nodes = $total"
echo ""
echo "################################################"
echo "queue      maxlimit     used      free"

if [ $short1 ] ; then
echo -e "------------------------------------------------"
echo -e "short1\t\t90\t$short1\t$((90-$short1))"  
fi

if [ $short2 ] ; then
echo -e "------------------------------------------------"
echo -e "short2\t\t64\t$short2\t$((64-$short2))"
fi

if [ $medium1 ] ; then
echo -e "------------------------------------------------"
echo -e "medium1\t\t32\t$medium1\t$((32-$medium1))"
fi

if [ $medium2 ] ; then
echo -e "------------------------------------------------"
echo -e "medium2\t\t64\t$medium2\t$((64-$medium2))"
fi

echo -e "------------------------------------------------"
echo -e "----------------User's Info---------------------"

if [ $nahlawat ] ; then
echo -e "------------------------------------------------"
echo -e "nahlawat\t50\t$nahlawat\t$((50-$nahlawat))"
fi

if [ $rasenjit ] ; then
echo -e "------------------------------------------------"
echo -e "rasenjit\t50\t$rasenjit\t$((50-$rasenjit))"
fi

if [ $sdas ] ; then
echo -e "------------------------------------------------"
echo -e "sdas\t\t50\t$sdas\t$((50-$sdas))"
fi

if [ $rajesh ] ; then
echo -e "------------------------------------------------"
echo -e "rajesh\t\t50\t$rajesh\t$((50-$rajesh))"
fi

if [ $changdev ] ; then
echo -e "------------------------------------------------"
echo -e "changdev\t50\t$changdev\t$((50-$changdev))"
fi

echo "################################################"
echo " "
