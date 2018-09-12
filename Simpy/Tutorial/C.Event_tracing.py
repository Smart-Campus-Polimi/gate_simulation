'''
you also want to trace which process created an event and which processes waited for an event.
The two most interesting functions for these use-cases are Environment.step(), where all events get processed, and Environment.schedule(), where all events get scheduled and inserted into SimPy’s event queue.
'''

from functools import partial, wraps
import simpy

def trace(env, callback):
	'''
	Replace the ``step()`` method of *env* with a tracing function
    that calls *callbacks* with an events time, priority, ID and its
	instance just before it is processed.
	'''
	def get_wrapper(env_step, callback):
		@wraps(env_step)
		def tracing_step():
			'''
			Call *callback* per il prossimo evento se ne esiste uno prima della
			chiamata a env.step()
			'''
			if len(env._queue):
				t, prio, eid, event = env._queue[0]
				callback(t, prio, eid, event)
			return env_step()
		return tracing_step

	env.step = get_wrapper(env.step, callback)

def monitor(data, t, prio, eid, event):
	data.append((t, eid, type(event)))

def test_process(env):
	yield env.timeout(1)

##############################################################
data = []
monitor = partial(monitor, data)
env = simpy.Environment()

trace(env, monitor)
p = env.process(test_process(env))
env.run(until = p)

for d in data:
	print(d)


'''
Using the same concepts, you can also patch Environment.schedule(). 
This would give you central access to the information when which event is scheduled for what time.
'''