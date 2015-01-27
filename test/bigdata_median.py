#!/usr/bin/env python

import random

num_count = 5000000
array_count = 5000

arrays = [[] for i in range(array_count)]
array_tot = []

for i in range(num_count):
	v = random.randint(0, num_count*2)
	i = random.randint(0, array_count-1)	
	array_tot.append(v)
	arrays[i].append(v)

array_tot = sorted(array_tot)
for i in range(array_count):
	arrays[i] = sorted(arrays[i])

low_list = []
high_list = []
for i in range(array_count):
	low_list.append(arrays[i][0])
	high_list.append(arrays[i][len(arrays[i])-1])
low_list = sorted(low_list)
high_list = sorted(high_list)

median = sorted([arrays[i][len(arrays[i])/2] for i in range(array_count)])[array_count/2]

print "[REAL]\t\tLow: {0}\tHigh: {1}\tMedian: {2}".format(array_tot[0], array_tot[num_count-1], array_tot[len(array_tot)/2])
print "[CALC]\t\tLow: {0}\tHigh: {1}\tMedian: {2}".format(low_list[0], high_list[len(high_list)-1], median)