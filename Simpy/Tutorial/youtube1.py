import simpy 

def main():
	env = simpy.Environment()
	env.process(traffic_light(env))
	env.run(until=300)
	print ("Simulation complete")


def traffic_light(env):
	while True:
		print("Light turned GREEN at t = "+str(env.now))
		yield env.timeout(30)
		print("Light turned YELLOW at t = "+str(env.now))
		yield env.timeout(5)
		print("Light turned RED at t = "+str(env.now))
		yield env.timeout(20)

if __name__ == '__main__':
	main()