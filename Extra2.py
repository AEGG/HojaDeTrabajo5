import random
import simpy

RANDOM_SEED = 2
PROCESS = 200 
INTERVAL_CPU = 5.0  
MIN_PROCESS = 0 
MAX_PROCESS = 3

def ready(env, number, interval, counter):
    for i in range(number):
        RAMGen = random.randint (1,100)
        c = proceso(env, 'Process%02d' % i, counter, RAMGen, time_Processed=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def monitorCPU(env, name):
    global ProRandomized, RAMQn, RAMGen
    ProRandomized = random.randint (1,2)
    if ProRandomized == 1:
        if RAMQn.level == MAX_PROCESS:
            print('Waiting Mode >>>')
            env.process(Tank(env))
        else:
            print('Pass-On >>>')
            env.process(proceso(env, name, counter, RAMGen, time_Processed))                
    else:
        env.process(ready(env, PROCESS, INTERVAL_CPU, counter))
        print('Continue >>>')

def Tank(env):
    yield env.timeout(1)
    print('Delaying por terminating rest Process >/<')
    env.process(ready(env, PROCESS, INTERVAL_CPU, counter))    

def proceso(env, name, counter, RAMGen, time_Processed):
    global profilerSim
    monitorCPU(env, name)    
    arrive = env.now
    print('%7.4f RAM: %7.4f %s: Process arrived' % (arrive, RAMGen, name))
    
    with counter.request() as req:
        procesoTo = random.uniform(MIN_PROCESS, MAX_PROCESS)
        results = yield req | env.timeout(RAMGen)

        wait = env.now - arrive
        profilerSim = profilerSim + wait

        if req in results:
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_Processed)
            yield env.timeout(tib)
            print('%7.4f %s: Completed' % (env.now, name))
            
        else:
            print('%7.4f %s: Altered/Ran after %6.3f' % (env.now, name, wait))

print('Sys. Boot')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
RAMQn = simpy.Container(env, init=3, capacity=100)
env.process(ready(env, PROCESS, INTERVAL_CPU, counter))
profilerSim = 0
env.run()
print "Tiempo total de Corrida: " , profilerSim, "promedio: " , profilerSim/25.0

