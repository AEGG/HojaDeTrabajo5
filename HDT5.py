"""
Hoja de Trabajo 5
Aaron Giron 13042
Kuk Chung 13279
22/08/14
"""

import random
import simpy


RANDOM_SEED = 42
PROCESS = 25  # numero de procesos
INTERVAL_PROCESS = 1.0  # Generate new customers roughly every x seconds
MIN_PROCESS = 0  # Min. customer patience
MAX_PROCESS = 3  # Max. customer patience



def source(self, env, number, interval, counter):
    """Source generates customers randomly"""
    
    for i in range(number):
        c = proceso(env, 'Proceso%02d' % i, counter, time_process=10.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def customer(env, name, counter, time_process):
    global promedio
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))
    
    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

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
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
promedio = 0
env.run()
print "tiempo total de espera: " , promedio, "promedio: " , promedio/5.0

