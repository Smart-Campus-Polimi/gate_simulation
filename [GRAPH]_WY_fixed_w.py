import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# definition of MAPE 
def MAPE(y_true, y_pred):
	m = []
	y_true, y_pred = np.array(y_true), np.array(y_pred)
	for i in range(0, len(y_true)):
		for j in range(0, len(y_pred)):
			if y_true[i][j] != 0:
				m.append(np.abs((y_true[i][j] - y_pred[i][j])/y_true[i][j]))
	
	m = np.array(m)
	return np.mean(m) * 100


INPUT_PATH = "/home/daniubo/Scrivania/gate_simulation/WY/fixed_w/"
INPUT_PATH_100 = "/home/daniubo/Scrivania/gate_simulation/matrices_for_errors/"

mean_list = []
mape_list = []
NUM_REALIZATION = 1
while NUM_REALIZATION < 11:
	wrong_mat = np.loadtxt(INPUT_PATH + str(NUM_REALIZATION) + "_100.csv", dtype = float, delimiter = ",")
	hundred_mat = np.loadtxt(INPUT_PATH_100 + str(NUM_REALIZATION) + "realization/" + "100percent_mac_matrix.csv", dtype = int, delimiter = ",")
	dist = np.linalg.norm(hundred_mat - wrong_mat)
	mape = MAPE(hundred_mat, wrong_mat)
	mean_list.append(dist)
	mape_list.append(mape)
	NUM_REALIZATION += 1

mean = np.mean(mean_list)
mape = np.mean(mape_list)
print("############################################################\n")
print("Accuracy with fixed weights and errors (W*Y method): "+str(100-mape)+"\n")
print("Mape: "+str(mape)+"\tNorm: "+str(mean)+"\n")
print("############################################################\n")
	