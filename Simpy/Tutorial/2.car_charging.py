#coding=utf-8

'''
Lets assume that the car from our last example magically became an electric vehicle. 
Electric vehicles usually take a lot of time charging their batteries after a trip. 
They have to wait until their battery is charged before they can start driving again.

The run process is automatically started when Car is instantiated. 
A new charge process is started every time the vehicle starts parking.
'''

import simpy as sp

class Car(object):
	def __init__(self, env):
		self.env = env
		# ogni volta che creo un auto, run() viene eseguita
		self.action = env.process(self.run())

	def run(self):

		while True:
			print("Start parking and charging at ", self.env.now)
			charge_duration = 5;
			# diamo la precedenza al processo che la funzione process() ritorna
			# aspettiamo finchè finisce
			try:
				yield self.env.process(self.charge(charge_duration))
			except sp.Interrupt:
				#quando riceviamo un Interrupt, stoppiamo la carica e mettiamo in driving state
				print(">>> Charge interrupted. Full enough? ")

			# il processo di ricarica è finito e possiamo riprendere a guidare
			print ("Start driving at ", self.env.now)
			trip_duration = 2
			yield self.env.timeout(trip_duration)


	def charge(self, duration):
		yield self.env.timeout(duration)

def driver(env, car):
	yield env.timeout(3)
	# dopo aver atteso 3 istanti temporali, interrompe la carica dell'auto
	car.action.interrupt()


'''
Qui inizia l'esecuzione del programma 
'''
env = sp.Environment();
car = Car(env)
env.process(driver(env, car))
env.run(until = 20)
