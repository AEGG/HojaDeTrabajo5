
import random
import simpy

RANDOM_SEED = 2
PROCESS = 25  
INTERVAL_CPU = 1.0  
MIN_PROCESS = 0 
MAX_PROCESS = 3

def ready(env, number, interval, counter):
    for i in range(number):
        c = proceso(env, 'Process%02d' % i, counter, time_Processed=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def proceso(env, name, counter, time_Processed):
    global profilerSim    
    arrive = env.now
    print('%7.4f %s: Process arrived' % (arrive, name))

    with counter.request() as req:
        procesoTo = random.uniform(MIN_PROCESS, MAX_PROCESS)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(procesoTo)

        wait = env.now - arrive
        profilerSim = profilerSim + wait

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_Processed)
            yield env.timeout(tib)
            print('%7.4f %s: Completed' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: Altered/Ran after %6.3f' % (env.now, name, wait))

# Setup and start the simulation
print('Sys. Boot')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
RAMQn = simpy.Container(env, capacity=100)
env.process(ready(env, PROCESS, INTERVAL_CPU, counter))
profilerSim = 0
env.run()
print "Tiempo total de Corrida: " , profilerSim, "promedio: " , profilerSim/25.0
