import random, math
import numpy as np
import scipy as sp
import scipy.stats as stats
import matplotlib.pyplot as plt
import SimPy.Simulation as Sim

class G:
	'''
	Class for global variables
	'''
	maxTime = 24.0 # hours
	arrivalrate = 100 # per hour
	parkingtime = 2.0 # hours
	parkedcars = 0
	seedVal = 9999

class Arrival(Sim.Process):
	""" Source generates cars at random
	Arrivals are at a time-dependent rate
	"""
	def generate(self):
		i=0
		while (self.sim.now() < G.maxTime):
			tnow = self.sim.now()
			arrivalrate = 100 + 10 * math.sin(math.pi * tnow/12.0)
			t = random.expovariate(arrivalrate)
			yield Sim.hold, self, t
			c = Car(name="Car%02d" % (i), sim=self.sim)
			timeParking = random.expovariate(1.0/G.parkingtime)
			self.sim.activate(c, c.visit(timeParking))
			i += 1

class Car(Sim.Process):
	""" Cars arrives, parks for a while, and leaves
	Maintain a count of the number of parked cars as cars arrive and leave
	"""
	def visit(self, timeParking=0):
		self.sim.parkedcars += 1
		self.sim.parking.observe(self.sim.parkedcars)
		yield Sim.hold, self, timeParking
		self.sim.parkedcars -= 1
		self.sim.parking.observe(self.sim.parkedcars)

class Parkingsim(Sim.Simulation):
	def run(self, aseed):
		random.seed(seed)
		Sim.initialize()
		s = Arrival(name='Arrivals', sim=self)
		self.parking = Sim.Monitor(name='Parking', ylab='cars', tlab='time', sim=self)
		self.activate(s, s.generate(), at=0.0)
		self.simulate(until=G.maxTime)


parkinglot = Parkingsim()
parkinglot.run(1234)

plt.figure(figsize=(5.5,4))
plt.plot(parkinglot.parking.tseries(),parkinglot.parking.yseries())
plt.xlabel('Time')
plt.ylabel('Number of cars')
plt.xlim(0, 24)
