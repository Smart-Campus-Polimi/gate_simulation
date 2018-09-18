import numpy as np

NUM_OF_REALIZATION = 2

INPUT_PATH = "/home/daniubo/Scrivania/gate_simulation/matrices_for_errors/"+str(NUM_OF_REALIZATION)+"realization/"
OUTPUT_PATH = "/home/daniubo/Scrivania/gate_simulation/WY/variable_w/no_errors/"

n_mac = { 10: 15,
		  20: 30,
		  30: 45,
		  40: 60,
		  50: 75,
		  60: 90,
		  70: 105,
		  80: 120,
		  90: 135,
		  100: 150	
}


while NUM_OF_REALIZATION < 11:
	PERCENTAGE = 100
	while PERCENTAGE > 0:
		
		INPUT_PATH = "/home/daniubo/Scrivania/gate_simulation/matrices/"+str(NUM_OF_REALIZATION)+"realization/"
		#gate_matrix = np.loadtxt(INPUT_PATH + 'gate_matrix.csv', dtype = int, delimiter = ",")
		#system_number = 0
		#for i in range(0,len(gate_matrix)):
		#	for j in range(0, len(gate_matrix)):
		#		system_number = system_number + gate_matrix[i][j]
		#print("Realization "+str(NUM_OF_REALIZATION)+":", system_number, "\n")
		
		mac_matrix = np.loadtxt(INPUT_PATH+str(PERCENTAGE)+'percent_matrix.csv', dtype = int, delimiter = ",")
		WY_matrix = np.array([[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]])
		weights_matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
		weights_matrix = mac_matrix/n_mac[PERCENTAGE]
		#print("##########################")
		#print("Counted matrix:\n")
		#print(mac_matrix)
		#print("\nWeights matrix:\n")
		#print(weights_matrix)
		#print("\nReal Matrix:\n")
		#print(real_matrix)

		
		for i in range(0,len(weights_matrix)):
			for j in range(0, len(weights_matrix)):
				WY_matrix[i][j] = weights_matrix[i][j]*n_mac[100]
		print("############# weights_matrix ###########\n")
		print(weights_matrix)
		print("############# WY #################\n")
		print(WY_matrix)
		print("############# Real matrix ###############\n")
		print(mac_matrix)
		print("##########################################\n##########################################\n")
		np.savetxt(OUTPUT_PATH + str(NUM_OF_REALIZATION) + '_' + str(PERCENTAGE)+ '.csv', WY_matrix, delimiter=',', fmt = '%0.2f') 
		PERCENTAGE -= 10	
	NUM_OF_REALIZATION +=1	
