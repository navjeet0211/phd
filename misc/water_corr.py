## To calculate residence time of active site water in hrab21 ##

import sys

import time
start = time.time()

fileName = sys.argv[1]

time = []
water = []

#make two 1d arrays for time and water

with open(fileName, "r") as input:
    for line in input:
        time.append(line.split()[0])
        water.append(line.split()[1])

# define a totaltimescale in picoseconds - the minus 1 is 
# because of the zero index
# windowsize is 2 ns

totaltimescale = 50000 - 1
windowsize = 2000

# endtau should take into consideration the multiplier
# below so 400 with a multiplier of 5 gives us 

endtau = 400
alltau = range(1, endtau)

for tau in alltau:

# there is a tau multiplier (i.e. use every 5th tau
# or every 5 picoseconds to speed up calculation)

    tau = 5*tau
    print tau

# these three values just start counters

    counter = 0
    noncounter = 0
    output = 0

# to set up a value for total number of windows we're interested in,
# leave off 2 times the windowsize at the end arbitrarily so it doesn't 
# jump too far, may get errors eventually for this so may have to be wary

    numberofwindows = totaltimescale - 2*windowsize
    listofwindowstartingpoints = range(0, numberofwindows)

# outer iterator which ensures the window (of size start - start + windowsize)
# is moved down one unit each time, i.e. starts at the next picosecond
'''
    for startingpoint in listofwindowstartingpoints:
        window = range(startingpoint, startingpoint + windowsize)
        for a in window:
            if a + tau < totaltimescale:
                if water[a] == water[a + tau]:
                counter = float(counter + 1)
                else:
                    noncounter = noncounter + 1
                totaljumpsanalysed = float(counter + noncounter)
                output = counter/totaljumpsanalysed
            else:
                pass
'''

    totaljumpsanalysed = 0
    for startingpoint in listofwindowstartingpoints:
        window = range(startingpoint, startingpoint + windowsize)
        for a in window:
            if a + tau < totaltimescale:
                if water[a] == water[a + tau]:
                    counter += 1
                totaljumpsanalysed += 1

    output = float(counter)/float(totaljumpsanalysed)

# counters should have kept values

    print counter
    print totaljumpsanalysed
    print output

    with open(fileName + '.autocorrelate', "a") as outfile:
        outfile.writelines('{0}     {1}{2}'.format(tau, output, '\n'))

print 'It took', time.time()-start, 'seconds.'
