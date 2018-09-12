import xml.etree.cElementTree as ET
from random import randint

edges = {}

# function to build the dictionary containing all the possible edges
def build_the_dict():
	global edges
	edges["0"] = "GiuriatitoDEIB"
	edges["1"] = "DEIBtoGolgi"
	edges["2"] = "GolgitoGiuriati"
	edges["3"] = "GiuriatitoPonzio"
	edges["4"] = "PonziotoDEIB"
	edges["5"] = "DEIBtoGiuriati"
	edges["6"] = "GiuriatitoGolgi"
	edges["7"] = "GolgitoPonzio"
	edges["8"] = "PonziotoGolgi"
	edges["9"] = "GolgitoDEIB"
	edges["10"] = "DEIBtoPonzio"
	edges["11"] = "PonziotoGiuriati"

'''
	function to build the path of each person walking through the network;
	the length of the path is fixed equal to 2 because it seems unlikely that 
	a person enter to a gate and then takes two edges to reach another one instead
	of the shortest route
'''
def build_the_random_path():
	global edges
	n_old = 0
	nplusOne = 0
	length_of_path = 2
	#print(length_of_path)
	edges_of_the_path = []
	for i in range(0,length_of_path):
		if i == 0:
			#print (">>> primo edge")
			n_old = str(randint(1,11))
			edges_of_the_path.append(edges[n_old])
		else:
			#print(">>> provo ad allungare il path")
			nplusOne = (int(n_old) + 1) % 12
			#print(">>> Riuscito, path lungo: ", len(edges_of_the_path))
			edges_of_the_path.append(edges[str(nplusOne)])
			n_old = nplusOne

	return edges_of_the_path

def single_string_path(path):
	single_string = "";
	flag = 0
	for element in path:
		if flag == 0:
			single_string = single_string + str(element)
			flag = 1
		else: 
			single_string = single_string + " " + str(element)
	print (single_string)
	return single_string

# build the dictionary of edges
build_the_dict()

# start writing the xml file
root = ET.Element("routes")

for i in range(0,30):
	departure = 0 + (10*i)
	path = build_the_random_path()
	path = single_string_path(path)
	doc = ET.SubElement(root, "person", id="person"+str(i), depart=str(departure), color="0,0,1")
	ET.SubElement(doc, "walk", edges=path)


tree = ET.ElementTree(root)
tree.write("gate.rou.xml")


