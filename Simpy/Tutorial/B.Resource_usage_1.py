'''
Estremo opposto del caso precedente: monitorare esattamente un use case. 
Ad esempio, sapere solamente quanti processi sono in attesa per una certa risorsa per ogni istante temporale.
'''
import simpy

class Monitored_Resource(simpy.Resource):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data = []

	def request(self, *args, **kwargs):
		self.data.append((self._env.now, len(self.queue)))
		return super().request(*args, **kwargs)

	def release(self, *args, **kwargs):
		self.data.append((self._env.now, len(self.queue)))
		return super().release(*args, **kwargs)

def test_process(env, res):
	with res.request() as req:
		yield req
		yield env.timeout(1)

###############################################################
env = simpy.Environment()

res = Monitored_Resource(env, capacity = 1)
p1 = env.process(test_process(env, res))
p2 = env.process(test_process(env, res))

env.run()

print(res.data)