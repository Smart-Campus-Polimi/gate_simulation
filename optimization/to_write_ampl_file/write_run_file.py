import numpy as np
from shutil import copyfile

NUM_REALIZATION = 1
PERCENTAGE = 100

while NUM_REALIZATION < 11:
	PERCENTAGE = 100
	while PERCENTAGE > 0:
		copyfile("/home/daniubo/Scrivania/simulation_part/optimization/to_write_ampl_file/lp_base.run","/home/daniubo/Scaricati/ampl.linux64/lp_run_"+str(NUM_REALIZATION)+"_"+str(PERCENTAGE)+".run")
		with open("/home/daniubo/Scaricati/ampl.linux64/lp_run_"+str(NUM_REALIZATION)+"_"+str(PERCENTAGE)+".run", 'a') as f:
			f.write("data /home/daniubo/Scaricati/ampl.linux64/lp_dat_"+str(NUM_REALIZATION)+"_"+str(PERCENTAGE)+".dat;\n")
			f.write("option solver \"./cplex\";\n");
			f.write("solve;\n")
			f.write("display x > mat_"+str(NUM_REALIZATION)+"_"+str(PERCENTAGE)+".txt;")

		PERCENTAGE -= 10
	NUM_REALIZATION += 1

