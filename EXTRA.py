
import random
import simpy

RANDOM_SEED = 2
PROCESS = 10 
INTERVAL_CPU = 1.0  
MIN_PROCESS = 0 
MAX_PROCESS = 3

def ready(env, number, interval, counter):
    for i in range(number):
        c = proceso(env, 'Process%02d' % i, counter, time_Processed=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def monitorCPU(env, name):
    global ProRandomized
    ProRandomized = random.randint(1,2)
    if ProRandomized == 1:
        if RAMQn.level == MAX_PROCESS:
            print('%7.4f %s: Waiting Mode >>>' % (arrive, name))
            env.process(Tank(env, CPUFlow))
        else:
            print('%7.4f %s: Pass-On >>>' % (arrive, name))
            env.process(ready(env, PROCESS, INTERVAL_CPU, counter))                
    else:
        # env.process(ready(env, PROCESS, INTERVAL_CPU, counter))
        print('Continue >>>')

def Tank(env, CPUFlow):
    yield env.timeout(MIN_PROCESS)
    print('%7.4f %s: Delaying por terminating rest Process >/<' % (arrive, name))

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
RAMQn = simpy.Container(env, init=3, capacity=100)
env.process(ready(env, PROCESS, INTERVAL_CPU, counter))
#env.process(monitorCPU(env))
profilerSim = 0
env.run()
print "Tiempo total de Corrida: " , profilerSim, "promedio: " , profilerSim/25.0
