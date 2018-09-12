import numpy as np
from random import randint

NUM_OF_REALIZATION = 1
percentage = 10
count_perc = 1

#start_mat = np.loadtxt('/home/daniubo/Scrivania/simulation_part/matrices/'+str(NUM_OF_REALIZATION)+'realization/100percent_matrix.csv', dtype = int, delimiter = ",")

while NUM_OF_REALIZATION<11:
	start_mat = np.loadtxt('/home/daniubo/Scrivania/simulation_part/matrices_for_errors/'+str(NUM_OF_REALIZATION)+'realization/100percent_mac_matrix.csv', dtype = int, delimiter = ",")
	count = 0
	count_perc = 1
	while count != 135:
		x = 0
		y = 0
		while x==y:
			x = randint(0,3)
			y = randint(0,3)
		if start_mat[x][y] > 0:
			start_mat[x][y] -= 1
			count = count + 1
			if count%15==0:
				np.savetxt('/home/daniubo/Scrivania/simulation_part/matrices_for_errors/'+str(NUM_OF_REALIZATION)+'realization/'+str(100-count_perc*percentage)+'percent_mac_matrix.csv', start_mat, delimiter=',', fmt = '%0.0f') 
				count_perc += 1
	NUM_OF_REALIZATION += 1

