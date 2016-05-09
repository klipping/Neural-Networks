import random as rd
import matplotlib.pyplot as plt
import math
import numpy as np

class Optim(object):
      def __init__(self, size):
            '''
            The init function genarates an arbitrary linear frequency - channel configuration called self.start
            @param size: the number of channels that have to be optimized for (always 40 for X-IFU)
            '''
            rd.seed()
            self.size = size
            self.start = np.array(range(size))
            self.pwr = 1
            self.lastdist = 0

      def changePwr(self, pwr):
            '''
            self.pwr is referred to as 'b' in the thesis, is of importance for the distance metric
            '''
            self.pwr = pwr

      ## together distanceN and distance make up the distance metric and caculate the 'total distance'
      
      def distanceN(self, item, r):
            dist = np.absolute(item - np.append(item[r:],item[0:r]))
            return(np.sum(np.power(dist,self.pwr)))

      def distance(self, item, r):
            dist = 0
            for i in range(r):
                  dist += (1.0/((i+1)**2))*self.distanceN(item,i+1)
            return(dist)

      def evolution(self, steps,tries, c, r):
            ## evolution changes two frequency coupled channels and checks if this new layout is better
            ## than the old, it does this "steps" times.
            maxD = 0
            if c == 1:
                  for i in range(tries):
                        rd.seed()
                        dist = 0
                        ld=0
                        start = self.start.copy()
                        for j in range(steps):
                              r1 = rd.randint(1,self.size - 1)
                              r2 = rd.randint(1,self.size - 1)
                              temp = start.copy()
                              temp[r1] = start[r2]
                              temp[r2] = start[r1]
                              dist = self.distance(temp, r)
                              if dist > ld:
                                    start = temp
                                    ld = dist
                        if ld > maxD:
                              maxF = start 
                              maxD = ld
                        print(start)
            self.start = maxF
            self.maxd = maxD
            return(maxF, self.maxd)

      def animal(self):
            ## animal repeats evolution various times in parallel 
            F1, D1 = self.evolution(100,10, 1, 3)
            print(D1)
            F2, D2 = self.evolution(1000,4,1,3)
            print(D2)
            F3, D3 = self.evolution(10000,4,1, 3)
            print(D3)
            F4, D4 = self.evolution(100000,1,1, 3)
            print(D4)
            return(F4, D4)

## plotting example
for i in range(5):
      x = Optim(40)
      x.changePwr(1/3.0)
      plotra = x.animal()[0]
      plt.plot(plotra,'ro')
      plt.plot(plotra, 'k')
plt.savefig('anna.pdf')
plt.show()
