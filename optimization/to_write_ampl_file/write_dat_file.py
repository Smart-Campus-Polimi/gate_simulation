import numpy as np
from shutil import copyfile


Y_index = ['i1', 'o1', 'i2', 'o2', 'i3', 'o3', 'i4', 'o4']


NUM_OF_REALIZATION = 1
while NUM_OF_REALIZATION < 11:
	PERCENTAGE = 100
	while PERCENTAGE > 0:

		INPUT_PATH = "/home/daniubo/Scrivania/simulation_part/matrices_for_errors/"+str(NUM_OF_REALIZATION)+"realization/"
		
		Y = np.loadtxt(INPUT_PATH+"Y.csv", dtype = int, delimiter = ",")
		copyfile("/home/daniubo/Scrivania/simulation_part/optimization/to_write_ampl_file/lp_base.dat","/home/daniubo/Scrivania/simulation_part/optimization/to_write_ampl_file/lp_dat_"+str(NUM_OF_REALIZATION)+'_'+str(PERCENTAGE)+"_just_Y.dat")
		with open("/home/daniubo/Scrivania/simulation_part/optimization/to_write_ampl_file/lp_dat_"+str(NUM_OF_REALIZATION)+'_'+str(PERCENTAGE)+"_just_Y.dat", 'a') as f:
			f.write("\nparam:	Y :=\n")
			for i in range(0, len(Y)):
				f.write(Y_index[i]+"\t"+str(Y[i])+"\n")
			f.write(";\n")
		
		
		mat = np.loadtxt(INPUT_PATH+str(PERCENTAGE)+'percent_mac_matrix.csv', dtype = int, delimiter = ",")
		copyfile("/home/daniubo/Scrivania/simulation_part/optimization/to_write_ampl_file/lp_dat_"+str(NUM_OF_REALIZATION)+'_'+str(PERCENTAGE)+"_just_Y.dat", "/home/daniubo/Scrivania/simulation_part/optimization/to_write_ampl_file/lp_dat_"+str(NUM_OF_REALIZATION)+'_'+str(PERCENTAGE)+".dat")
		with open("/home/daniubo/Scrivania/simulation_part/optimization/to_write_ampl_file/lp_dat_"+str(NUM_OF_REALIZATION)+'_'+str(PERCENTAGE)+".dat", 'a') as f:
			f.write("\nparam:	s :=\n")
			for i in range(0,len(mat)):
				for j in range(0,len(mat)):
					
					if i!=j:
						#print(i+1, " ", j+1, "\t", str(mat[i][j]),  "\n")
						f.write(str(i+1)+" "+str(j+1)+"\t\t"+str(mat[i][j])+"\n")
			f.write(";\n")

			#comment this part if there are no weights
			##########################################
			'''
			f.write("\nparam: w :=\n")
			f.write("1 2\t0.080\n")
			f.write("1 3\t0.060\n")
			f.write("1 4\t0.073\n")
			f.write("2 1\t0.073\n")
			f.write("2 3\t0.107\n")
			f.write("2 4\t0.080\n")
			f.write("3 1\t0.087\n")
			f.write("3 2\t0.093\n")
			f.write("3 4\t0.060\n")
			f.write("4 1\t0.093\n")
			f.write("4 2\t0.087\n")
			f.write("4 3\t0.107\n")
			f.write(";\n")
			'''
			###########################################
		

		PERCENTAGE -= 10
	NUM_OF_REALIZATION += 1