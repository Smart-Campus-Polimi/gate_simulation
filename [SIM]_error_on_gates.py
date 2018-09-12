from random import randint
import random
import math
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt
import simpy as sim
import pandas as pd
import paho.mqtt.client as mqtt
import MySQLdb
import datetime

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

gate0_in = 0
gate0_out = 0
gate1_in = 0
gate1_out = 0
gate2_in = 0
gate2_out = 0
gate3_in = 0
gate3_out = 0

flux_matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
flux_matrix_prior = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

people_list = []
starting_time_list = []
durationOfTheTrip_list = []
sources = []
destinations = []

START_TIME = 16
BROKER_ADDRESS = "127.0.0.1"
TOPIC = "sim"

############################################
client = mqtt.Client('simulation_client')
client.connect(BROKER_ADDRESS)
############################################

MAX_TIME = 3600	#seconds
ARRIVAL_RATE = 20	#people per seconds
SEED = 9999		#seme della serie random 
VELOCITY = 5 	#metres per second
MAX_PEOPLE = 150
MAC_PERCENTAGE = 100
ERROR_PERCENTAGE = 5
err = 1
how_many_errors = MAX_PEOPLE*ERROR_PERCENTAGE/100
COUNT_ERROR_PEOPLE = 0


#db = MySQLdb.connect(host=BROKER_ADDRESS, user = "root", passwd = "root", db = "smartgateDB")
#cursor = db.cursor()
#cursor.execute("SET sql_mode=\'ANSI_QUOTES\'")

############################################################

# Series of functions to update the number of people passing through gates
def zero_in(n):
	global gate0_in
	gate0_in = gate0_in +1 +n 
	client.publish("sim", "[Gate0- IN]: 1")

def zero_out(n):
	global gate0_out
	gate0_out = gate0_out +1 +n
	client.publish("sim", "[Gate0- OUT]: 1")
	
def one_in(n):
	global gate1_in
	gate1_in = gate1_in +1 +n
	client.publish("sim", "[Gate1 - IN]: 1")

def one_out(n):
	global gate1_out
	gate1_out = gate1_out +1 +n
	client.publish("sim", "[Gate1 - OUT]: 1")

def two_in(n):
	global gate2_in
	gate2_in = gate2_in +1 +n
	client.publish("sim", "[Gate2 - IN]: 1")

def two_out(n):
	global gate2_out
	gate2_out = gate2_out +1 +n
	client.publish("sim", "[Gate2 - OUT]: 1")

def three_in(n):
	global gate3_in
	gate3_in = gate3_in +1 +n
	client.publish("sim", "[Gate3 - IN]: 1")

def three_out(n):
	global gate3_out
	gate3_out = gate3_out +1 +n
	client.publish("sim", "[Gate3 - OUT]: 1")

gates = {0 : zero_in,
         1 : one_in,
         2 : two_in,
         3 : three_in,
         4 : zero_out,
         5 : one_out,
         6 : two_out,
         7 : three_out,
}

links = {'01' : 0,
         '02' : 0,
         '03' : 0,
         '12' : 0,
         '13' : 0,
         '23' : 0,
}

'''
	function to build the path of each person walking through the network;
	the length of the path is fixed equal to 2 because it seems unlikely that 
	a person enter to a gate and then takes two edges to reach another one instead
	of the shortest route
'''
def build_precomputed_path(origin, destination):
	edges_of_the_path = []
	edges_of_the_path.append(str(origin))
	edges_of_the_path.append(str(destination))
	return edges_of_the_path

'''
function that update the counts of people per link
'''
def update_link_counts(origin, destination, error):
	if int(origin) < int(destination):
		link = str(origin) + str(destination)
		links[link] = links[link] + 1 + error
	else:
		link = str(destination) + str(origin)
		links[link] = links[link] + 1 + error

'''
function to update the counter of people entering through a certain gate
'''
def update_gate_in(n, error):
	global gates
	gates[n](error)

'''
function to update the counter of people exiting through a certain gate
'''
def update_gate_out(n, error):
	global gates
	gates[n+4](error)

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

# create a list of the timestamps when the person of the simulation starts
def build_list_of_starting_time(starting_time_list):
	official_time = []
	temp = []
	flag = 0
	for t in starting_time_list:
		m, s = divmod(t, 60)
		h, m = divmod(m, 60)
		if flag == 0:
			h = 16 + int(h)
			temp.append(int(h))
			temp.append(int(m))
			temp.append(round(s))
			flag = 1
		else:
			m, s = divmod(t, 60)
			h, m = divmod(m, 60)
			temp[0] = temp[0] + int(h)
			temp[1] = temp[1] + int(m)
			temp[2] = temp[2] + round(s)
			m, s = divmod(temp[2], 60)
			temp[2] = round(s)
			temp[1] = temp[1] + int(m)
			h, m = divmod(temp[1], 60)
			temp[1] = int(m)
			temp[0] = temp[0] + h
		timestring = "%d:%02d:%02d" % (temp[0], temp[1], temp[2])
		official_time.append(timestring)
	return official_time

# create a list with the time at which every person arrives at his destination
def build_list_of_ending_ts(starting_timestamps):
	data = []
	for i in range(0,MAX_PEOPLE):
		ts = starting_timestamps[i]
		seconds = int(ts[6:8])
		seconds = seconds + int(durationOfTheTrip_list[i])
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		temp = []
		temp.append(int(ts[0:2]) + int(h))
		temp.append(int(ts[3:5]) + int(m))
		temp.append(round(s))
		timestring = "%d:%02d:%02d" % (temp[0], temp[1], temp[2])
		data.append(timestring)
	return list(data)

#create lists with couple [start time, source] and [end time, stop]
def creating_queries_list(start, stop):
	inside = []
	outside = []
	for i in range(0,MAX_PEOPLE):
		temp_start = []
		temp_end = []
		temp_start.append(start[i])
		temp_start.append(sources[i])
		temp_end.append(stop[i])
		temp_end.append(destinations[i])
		inside.append(temp_start)
		outside.append(temp_end)
	return inside, outside

# delete duplicates primary keys in the list
def prepare_final_list_for_queries(complete_list):
	complete_list.sort()
	final_list = []
	flag = 0
	for element in complete_list:
		if flag == 0:
			final_list.append(element)
			flag = 1
		else:
			founded = 0
			for e in final_list:
				if element[0] == e[0] and element[1] == e[1]:
					e[2] = e[2] + element[2]
					e[3] = e[3] + element[3]
					founded = 1
			if founded == 0:
				final_list.append(element)
	return final_list

# build the list to create entries in the table every 3 minutes
def compacting_three_minutes(complete_list):
	max = 0
	step = 3
	flag = 0
	#found the max in minutes
	for element in complete_list:
		minutes = int(element[0][3:5])
		if minutes > max:
			max = minutes
	stop = (round(max/3)+1) * 3
	compact_list = []
	# build a list used to compact data
	for i in range(0, stop, step):
		ts = str(START_TIME) + ":" + str("%02d" %i) + ":" + "00"
		for j in range(0,4):
			temp = []
			temp.append(ts)
			temp.append(j)
			temp.append(0)
			temp.append(0)
			compact_list.append(temp)
	compact_list = compact_list[4:]
	# loop to compact the count of the people passed through each gate every 3 minutes
	for element in compact_list:
		for e in complete_list:
			if element[1] == e[1]:	#gate in questione uguale
				if int(element[0][3:5]) > 3:
					flag = 1
				if flag == 0:
					if int(e[0][3:5]) < int(element[0][3:5]) and int(element[0][0:2]) == int(e[0][0:2]):
						element[2] = int(element[2]) + int(e[2])
						element[3] = int(element[3]) + int(e[3])
				else:
					if int(e[0][3:5]) < int(element[0][3:5]) and int(e[0][3:5])>=(int(element[0][3:5])-3) and int(element[0][0:2]) == int(e[0][0:2]):
						element[2] = int(element[2]) + int(e[2])
						element[3] = int(element[3]) + int(e[3])
	return compact_list

'''
generate random MAC address
'''
def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def assign_MAC_address():
	how_many_mac = round(MAX_PEOPLE*MAC_PERCENTAGE/100);
	idS_with_mac = set()
	while len(idS_with_mac) != how_many_mac:
		idS_with_mac.add(randint(0, MAX_PEOPLE-1))
	return list(idS_with_mac)

# function that sends all the queries reguarding the simulation to the db
def sending_queries(data):
	for i in range(0, len(data)):
		ts = datetime.datetime.now().strftime("%Y-%d-%m") + " " +str(data[i][0])
		query = "INSERT INTO smartgateDB.flux_giorno (TimeStamp, Gate, Inside, Outside) VALUES ('"+ ts +"', '"+str(data[i][1])+"', '"+str(data[i][2])+"', '"+ str(data[i][3])+"')"
		cursor.execute(query)
		db.commit()

#create vector Y for the constrint of the LP model
def create_vector_y():
	temp = []
	temp.append(gate0_in)
	temp.append(gate0_out)
	temp.append(gate1_in)
	temp.append(gate1_out)
	temp.append(gate2_in)
	temp.append(gate2_out)
	temp.append(gate3_in)
	temp.append(gate3_out)
	return np.asarray(temp)

# Function used as source for generating people through the network
def source(env, flux_mat, interval, who_has_mac):
		"""Source generates customers based on the flux matrix"""
		count = 0
		rows = flux_mat.shape[0]
		cols = flux_mat.shape[1]
		for x in range(0,rows):
			for y in range(0,cols):
				if x != y:
					for i in range(0, flux_mat[x,y]):
						path = build_precomputed_path(x,y)
						temp = []
						temp.append(count + i)
						temp.append(int(path[0]))
						temp.append(int(path[1]))
						temp.append(randint(1,2))
						if (count+i) in who_has_mac:
							temp.append(rand_mac())
						else:
							temp.append(0)
						people_list.append(temp)
					count = count + flux_mat[x,y]
		random.shuffle(people_list)
		for p in people_list:
			pers = person(env, p[0], p[1], p[2], p[3], p[4])
			env.process(pers)
			t = random.expovariate(1.0 / interval)
			starting_time_list.append(float("%.2f" % t))
			sources.append(p[1])
			destinations.append(p[2])
			yield env.timeout(t)
		#print_statistics()

# Function creating people walking from origin to destination @ velocity = VELOCITY
def person(env, ID, origin, destination, velocity, mac_address):
	distance_to_walk = compute_distance(origin, destination)
	global how_many_errors, COUNT_ERROR_PEOPLE
	if how_many_errors > 0:
		COUNT_ERROR_PEOPLE += 1
		choice = random.choice([True, False])
		if choice:
			error = err
		else:
			error = err*(-1)
		flux_matrix[origin, destination] = flux_matrix[origin, destination] + 1 + error
		update_gate_in(origin, error)
		update_link_counts(origin, destination, error)
		#global how_many_errors
		how_many_errors = how_many_errors - 1
	else:
		error = 0
		flux_matrix[origin, destination] = flux_matrix[origin, destination] + 1 + error
		update_gate_in(origin, error)
		update_link_counts(origin, destination, error)
	if mac_address != 0:
		flux_matrix_prior[origin, destination] = flux_matrix_prior[origin, destination] + 1
	#view_information(ID, origin, destination, velocity, distance_to_walk)
	while True:
		#print("[PERSON",ID,"] I've started walking from", nodes[str(origin)])
		#if mac_address != 0: 
			#print("[PERSON",ID,"] My MAC address is: ", mac_address)
		durationOfTheTrip_list.append(round(distance_to_walk/velocity))
		yield env.timeout(round(distance_to_walk/velocity))
		#print("[PERSON",ID,"] I'm arrived @", nodes[str(destination)], "in", round(distance_to_walk/velocity), "seconds;\n>>> Updating gate counter...")
		if how_many_errors > 0:
			COUNT_ERROR_PEOPLE += 1
			if choice:
				error = err
			else:
				error = err*(-1)
			update_gate_out(destination, error)
			#global how_many_errors
			how_many_errors = how_many_errors - 1
		else:
			error = 0
			update_gate_out(destination, error)
		break;

# main function
def main():
	random.seed(randint(999,9999))
	who_has_mac = assign_MAC_address()
	print("I gate sbaglieranno "+str(how_many_errors)+" su 150 persone.\n")
	#per avere sempre stessi risultati usare variabile globale SEED
	flux_mat = np.loadtxt('flux_matrix.csv', dtype = int, delimiter = ",")
	env = sim.Environment()
	env.process(source(env, flux_mat, ARRIVAL_RATE, who_has_mac))
	env.run(until=MAX_TIME)
	print(">>>>>>>>>>>>>> Simulation complete")
	visualization_matrix = pd.DataFrame(flux_matrix, index=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'], columns=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'])
	visualization_matrix_mac = pd.DataFrame(flux_matrix_prior, index=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'], columns=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'])
	difference_mat = pd.DataFrame(flux_matrix - flux_matrix_prior, index=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'], columns=['Golgi', 'Giuriati', 'Ponzio', 'DEIB'])
	print("\n\n")
	print(visualization_matrix)
	print("\n\n")
	print(visualization_matrix_mac)
	print("\n\n")
	print(difference_mat)
	print("\n\n")
	print(">>> Errori inseriti: "+str(COUNT_ERROR_PEOPLE)+"\n")

	np.savetxt("/home/daniubo/Scrivania/simulation_part/matrices_for_errors/10realization/gate_matrix.csv", visualization_matrix, delimiter=",", fmt="%0.0f")
	np.savetxt("/home/daniubo/Scrivania/simulation_part/matrices_for_errors/10realization/100percent_mac_matrix.csv", visualization_matrix_mac, delimiter=",", fmt="%0.0f")

	Y = create_vector_y()
	np.savetxt("/home/daniubo/Scrivania/simulation_part/matrices_for_errors/10realization/Y.csv", Y.T, delimiter=",", fmt="%0.0f")

	print_statistics()

	# lista con tutti i ts di partenza degli utenti
	starting_timestamps = build_list_of_starting_time(starting_time_list)

	# lista con tutti i ts di arrivo degli utenti
	end_of_trip_timestamps = build_list_of_ending_ts(starting_timestamps)

	# lista con coppie instante-gate
	inside_for_queries, outside_for_queries = creating_queries_list(starting_timestamps, end_of_trip_timestamps)

	# riordinamento dei timestamp degli arrivi in quanto possono risultare disordinati 
	# in base alla velocità di percorrimento e la distanza da percorrere per ogni persona
	outside_for_queries.sort()

	inside_for_queries = [x + [1] + [0] for x in inside_for_queries]
	outside_for_queries = [x + [0] + [1] for x in outside_for_queries]

	complete_list = []
	for element in inside_for_queries:
		complete_list.append(element)
	for element in outside_for_queries:
		complete_list.append(element)

	complete_list = prepare_final_list_for_queries(complete_list)
	complete_list = compacting_three_minutes(complete_list)
	#sending_queries(complete_list)
	#for key, value in links.items():
		#print ("link: ", key,"\tcounts: ", value)

if __name__ == '__main__':
	main()