from functools import partial, wraps

import simpy

def patch_resource(resource, pre = None, post = None):
	'''
	Patch *resource* so that it calls the callable *pre* before each
    put/get/request/release operation and the callable *post* after each
    operation.  The only argument to these functions is the resource
    instance.
    '''
    def get_wrapper(func):
    	# genera un wrapper per metterci le put/get/request/release
    	@wraps(func)
    	def wrapper(*args, **kwargs):
    		if pre:
    			pre(resource)

    		ret = func(*args, **kwargs)

    		if post:
    			post(resource)

    		return ret
    	return wrapper

    for name in ['put', 'get', 'request', 'release']:
    	if hasattr(resource, name):
    		setattr(resource, name, get_wrapper(getattr(resource, name)))

def monitor(data, resource):
	# richiamo al monitoring
	item = (
		resource._env.now,		#tempo corrente della simulazione
		resource.count,			#numero di utenti
		len(resource.queue))	#numero di processi incodati
	data.append(item)

def test_process(env, res):
	with res.request() as req:
		yield req
		yield env.timeout(1)


##################################################################
env = simpy.Environment()
res = simpy.Resource(env, capacity = 1)
data = []
# lega *data* come primo argomento da monitorare con *monitor()*
monitor = partial(monitor, data)
patch_resource(res, post=monitor)

p = env.process(test_process(env, res))
env.run(p)

print (data)