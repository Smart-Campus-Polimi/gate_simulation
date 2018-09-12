#from amplpy import AMPL, Environment
#ampl = AMPL(Environment("/home/daniubo/Scaricati/ampl.linux64/"))

import subprocess
import shlex

NUM_REALIZATION = 1

while NUM_REALIZATION < 11:
	PERCENTAGE = 100
	while PERCENTAGE > 0:
		filename = "/home/daniubo/Scaricati/ampl.linux64/ampl /home/daniubo/Scaricati/ampl.linux64/lp_run_"+str(NUM_REALIZATION)+"_"+str(PERCENTAGE)+".run"
		path = shlex.split(filename)
		print("-------------------",NUM_REALIZATION, PERCENTAGE,"-------------------------------")
		subprocess.Popen(path)
		print("--------------------------------------------------------")

		#ampl.read("lp.mod")
		#ampl.readData("lp_dat_"+str(NUM_REALIZATION)+"_"+str(PERCENTAGE)+".dat")
		PERCENTAGE -= 10

	NUM_REALIZATION += 1