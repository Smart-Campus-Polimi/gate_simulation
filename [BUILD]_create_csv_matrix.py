import numpy as np

NUM_REALIZ = 1
PERCENTAGE = 100

INPUT_PATH_MATRICES = "/home/daniubo/Scaricati/ampl.linux64/no_errors_var_weights/matrices/"
OUTPUT_PATH = "/home/daniubo/Scrivania/gate_simulation/matrices/"

def oneTwo(n, flux_matrix):
	flux_matrix[0][1] = n;
	return

def oneThree(n, flux_matrix):
	flux_matrix[0][2] = n;
	return

def oneFour(n, flux_matrix):
	flux_matrix[0][3] = n;
	return

def twoOne(n, flux_matrix):
	flux_matrix[1][0] = n;
	return

def twoThree(n, flux_matrix):
	flux_matrix[1][2] = n;
	return

def twoFour(n, flux_matrix):
	flux_matrix[1][3] = n;
	return

def threeOne(n, flux_matrix):
	flux_matrix[2][0] = n;
	return

def threeTwo(n, flux_matrix):
	flux_matrix[2][1] = n;
	return

def threeFour(n, flux_matrix):
	flux_matrix[2][3] = n;
	return

def fourOne(n, flux_matrix):
	flux_matrix[3][0] = n;
	return

def fourTwo(n, flux_matrix):
	flux_matrix[3][1] = n;
	return

def fourThree(n, flux_matrix):
	flux_matrix[3][2] = n;
	return

update_mat = {	1 : oneTwo,
         		2 : oneThree,
         		3 : oneFour,
         		4 : twoOne,
         		5 : twoThree,
         		6 : twoFour,
         		7 : threeOne,
         		8 : threeTwo,
         		9 : threeFour,
         		10: fourOne,
         		11: fourTwo,
         		12: fourThree
}

while NUM_REALIZ < 11:
	PERCENTAGE = 100
	while PERCENTAGE > 0:
		flux_matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
		with open(INPUT_PATH_MATRICES + "mat_" + str(NUM_REALIZ) + "_" + str(PERCENTAGE) + ".txt", "r") as f:
			first_line = True
			count_line = 0
			for line in f:
				if not first_line and count_line < 12:
					count_line += 1
					flux = int(line[6:9])
					update_mat[count_line](flux, flux_matrix)
				else:
					first_line = False
		np.savetxt(OUTPUT_PATH+str(NUM_REALIZ)+"realization/"+str(PERCENTAGE)+"_matrix_variable_w.csv", flux_matrix, delimiter=",", fmt="%0.0f")
		PERCENTAGE -= 10
	NUM_REALIZ += 1