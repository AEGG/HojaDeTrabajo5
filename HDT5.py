"""
Hoja de Trabajo 5
Aaron Giron 13042
Kuk Chung 13279
22/08/14
"""

import random
import simpy


RANDOM_SEED = 42
random_seed = 2
PROCESS = 25  # numero de procesos
INTERVAL_PROCESS = 1.0  # Generate new customers roughly every x seconds
MIN_PROCESS = 0  # Min. customer patience
MAX_PROCESS = 3  # Max. customer patience

def init(self, env):
    self.counter = simpy.Resource(env, capacity=1)
    self.cpu = simpy.Container(env, init=0, capacity=100)
    
def monitor(self, env, router):
    while True:
        if self.cpu.level == 0:
            print('Process terminated %s' %env.now)

    router = random.randint(1,2)
    if router == 2:
        ready()
    else:
        waiting()
        
def waiting():
    print('Process waiting')    

def ready(self, env, number, interval, counter):
    for i in range(number):
        c = proceso(env, 'Proceso%02d' % i, counter, time_process=10.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def proceso(env, name, counter, time_process):
    global promedio
    arrive = env.now
    print('%7.4f %s: Proceso llegado' % (arrive, name))
    
    with counter.request() as req:
        PROCESS = random.uniform(MIN_PROCESS, MAX_PROCESS)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(PROCESS)

        wait = env.now - arrive
        promedio = promedio + wait
        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_process)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))

# Setup and start the simulation

random.seed(RANDOM_SEED)
random.seed(random_seed)
RAM = random.randint(1,10)
env = simpy.Environment()

# Start processes and run

env.process(ready(env, PROCESS, INTERVAL_PROCESS, ))
promedio = 0
env.run()
print "tiempo total de espera: " , promedio, "promedio: " , promedio/5.0

