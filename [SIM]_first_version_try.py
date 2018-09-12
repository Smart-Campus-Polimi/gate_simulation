from random import randint
import random
import math
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt
import simpy as sim
import pandas as pd

# Series of functions to update the number of people passing through gates
def zero_in():
	global gate0_in
	gate0_in = gate0_in +1 

def zero_out():
	global gate0_out
	gate0_out = gate0_out +1 

def one_in():
	global gate1_in
	gate1_in = gate1_in +1

def one_out():
	global gate1_out
	gate1_out = gate1_out +1 

def two_in():
	global gate2_in
	gate2_in = gate2_in +1 

def two_out():
	global gate2_out
	gate2_out = gate2_out +1 

def three_in():
	global gate3_in
	gate3_in = gate3_in +1

def three_out():
	global gate3_out
	gate3_out = gate3_out +1 

############################################################
nodes = {}
nodes["0"] = "Golgi"
nodes["1"] = "Giuriati"
nodes["2"] = "Ponzio"
nodes["3"] = "DEIB"


distances = {}
distances["0-1"] = 70
distances["1-0"] = distances["0-1"]
distances["0-2"] = 150
distances["2-0"] = distances["0-2"] 
distances["0-3"] = 80
distances["3-0"] = distances["0-3"]
distances["1-2"] = 60
distances["2-1"] = distances["1-2"]
distances["1-3"] = 40
distances["3-1"] = distances["1-3"]
distances["2-3"] = 50
distances["3-2"] = distances["2-3"]

gates = {0 : zero_in,
         1 : one_in,
         2 : two_in,
         3 : three_in,
         4 : zero_out,
         5 : one_out,
         6 : two_out,
         7 : three_out,
}

gate0_in = 0
gate0_out = 0
gate1_in = 0
gate1_out = 0
gate2_in = 0
gate2_out = 0
gate3_in = 0
gate3_out = 0

flux_matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

#people_list = []

MAX_TIME = 3600	#seconds
ARRIVAL_RATE = 20	#people per seconds
SEED = 9999		#seme della serie random 
VELOCITY = 5 	#metres per second
MAX_PEOPLE = 150

############################################################

'''
	function to build the path of each person walking through the network;
	the length of the path is fixed equal to 2 because it seems unlikely that 
	a person enter to a gate and then takes two edges to reach another one instead
	of the shortest route
'''
def build_the_random_path():
	global nodes
	n_old = 0
	nplusOne = 0
	length_of_path = 2
	edges_of_the_path = []
	for i in range(0,length_of_path):
		if i == 0:
			#print (">>> primo edge")
			n_old = str(randint(0,3))
			edges_of_the_path.append(n_old)
		else:
			#print(">>> provo ad allungare il path")
			nplusOne = str(randint(0,3))
			while(nplusOne == n_old):
				nplusOne = str(randint(0,3))
			#print(">>> Riuscito, path lungo: ", len(edges_of_the_path))
			edges_of_the_path.append(str(nplusOne))
	return edges_of_the_path

'''
function to update the counter of people entering through a certain gate
'''
def update_gate_in(n):
	global gates
	gates[n]()

'''
function to update the counter of people exiting through a certain gate
'''
def update_gate_out(n):
	global gates
	gates[n+4]()

# flux statistics during the simulation
def print_statistics():
	print("\n###################################\nSTATISTICS TILL NOW\n###################################")
	print("People entered from gate 0 [Golgi]:\t", gate0_in)
	print("People entered from gate 1 [Giuriati]:\t", gate1_in)
	print("People entered from gate 2 [Ponzio]:\t", gate2_in)
	print("People entered from gate 3 [DEIB]:\t", gate3_in)
	print("People exited from gate 0 [Golgi]:\t", gate0_out)
	print("People exited from gate 1 [Giuriati]:\t", gate1_out)
	print("People exited from gate 2 [Ponzio]:\t", gate2_out)
	print("People exited from gate 3 [DEIB]:\t", gate3_out)
	print("\n")



# Compute the distance between an origin and a destination for each people
def compute_distance(origin, destination):
	pathString = str(origin)+ "-" + str(destination)
	global distances
	distance = distances[pathString]
	return distance

# Show to the user all the infos about a person
def view_information(ID, origin, destination, velocity, distance):
    	print("Person", str(ID),"\ninformation:\n>>> Origin: ",origin,"\n>>> Destination: ",destination,"\n>>> Velocity: ", velocity,"\n>>> Distance: ", distance)


# Function used as source for generating people through the network
def source(env, number, interval):
		"""Source generates customers randomly"""
		for i in range(number):
			path = build_the_random_path()
			# velocita' randomizzata da 1 a 5 m/s, se si vuole tenerla costante, usare VELOCITY
			p = person(env, i, int(path[0]), int(path[1]), randint(1,2))
			'''
			temp = []
			temp.append(i)
			temp.append(int(path[0]))
			temp.append(int(path[1]))
			temp.append(VELOCITY)
			people_list.append(temp)
			'''
			env.process(p)
			t = random.expovariate(1.0 / interval)
			yield env.timeout(t)
			if (i%5 == 0):
				print_statistics()

# Function creating people walking from origin to destination @ velocity = VELOCITY
def person(env, ID, origin, destination, velocity):
	distance_to_walk = compute_distance(origin, destination)
	update_gate_in(origin)
	flux_matrix[origin, destination] = flux_matrix[origin, destination] + 1
	#view_information(ID, origin, destination, velocity, distance_to_walk)
	while True:
		print("[PERSON",ID,"] I've started walking from", nodes[str(origin)])
		yield env.timeout(round(distance_to_walk/velocity))
		print("[PERSON",ID,"] I'm arrived @", nodes[str(destination)], "in", round(distance_to_walk/velocity), "seconds;\n>>> Updating gate counter...")
		update_gate_out(destination)
		#print("[PERSON",ID,"] Finished my path!")
		break;

# main function
def main():
	random.seed(randint(999,9999))
	#per avere sempre stessi risultati usare variabile globale SEED
	env = sim.Environment()
	env.process(source(env, MAX_PEOPLE, ARRIVAL_RATE))
	env.run(until=MAX_TIME)
	print(">>>>>>>>>>>>>> Simulation complete")
	visualization_matrix = pd.DataFrame(flux_matrix, index=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'], columns=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'])
	print("\n\n")
	print(visualization_matrix)
	print("\n\n")
	print_statistics()
	#for p in people_list:
	#	print(p)


if __name__ == '__main__':
	main()