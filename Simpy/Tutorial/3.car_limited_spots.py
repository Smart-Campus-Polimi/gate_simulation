#coding=utf-8
'''
The car will now drive to a battery charging station (BCS) and request one of its two charging spots. 
If both of these spots are currently in use, it waits until one of them becomes available again.
It then starts charging its battery and leaves the station afterwards
'''
import simpy as sp

def car(env, name, bcs, driving_time, charge_duration):
	#simulate driving to the BSC
	yield env.timeout(driving_time)

	#request one of its charging spots
	print (name, " arriving at ", env.now)
	with bcs.request() as req:
		yield req

		# charge battery
		print (name, " starting to charge at ", env.now)
		yield env.timeout(charge_duration)
		print(name, " leaving the BCS at ", env.now)

'''
la risorsa viene rilasciata immediatamente se viene chiamata la request con 
il 'with' altrimenti, se non venisse chiamata così sarebbe necessaria
la chiamata della release().
Il modello base delle richieste è un FIFO.
'''

env = sp.Environment()
bcs = sp.Resource(env, capacity = 2)

for i in range(4):
	env.process(car(env, 'Car '+str(i), bcs, i*2, 5))

env.run()

