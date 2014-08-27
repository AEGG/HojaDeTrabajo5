# Universidad del Valle de Guatemala
# Algoritmos y Estructuras de Datos
# Seccion 30
# Aaron Giron 13042 / Kuk Ho Chung 13279
# Simulador de ejecucion de sistema operativo

# Importando las librerias de aleatoriedad y de simpy
import random
import simpy

# Definicion generalo de los variables iniciales
# para cantidad de procesos a ejcutar principalmente
RANDOM_SEED = 2
NEW_PROCESS = 200
INTERVAL_PROCESS = 1.0 

# Generador de los procesos con ciertas caracteristicas de requerimientos
def source(env, number, interval, RAM ,CPU, lagTime):
    for i in range(number):
        Inst = random.randint(1,10) # Aleatoriedad de las instrucciones
        memoryBlock = random.randint(1,10) # Aleatoriedad de la memoria a proveer para el proceso
        instGen = proceso(env, 'Process:%02d' % i, memoryBlock, RAM ,CPU, lagTime, Inst)
        env.process(instGen)
        tm = random.expovariate(1.0 / interval) 
        yield env.timeout(tm)

# Proceso general del programa de simulador de sistema operativo
def proceso(env, processID, memoryBlock, RAM, CPU, lagTime, Inst):
    global timeSim # Definicion para simular el profiler como para contar el tiempo de ejecucion del simulador
    arrive = env.now # Definicion de ambiente actual = tiempo, como una variable
    print('T: %7.4fs %s: Process/Instruction arrived >>' % (arrive, processID))
    print('T: %7.4fs %s: Requiring RAM %s / Available RAM  %s' % (arrive, processID, Inst, RAM.level)) 

    # Obtiene la memoria para el RAM como un dicho requerimiento
    with RAM.get(memoryBlock) as req:     
        yield req
        # Calculo de tiempo de espera alternamente
        wait = env.now - arrive        
        # Inicializacion de proceso y pide RAM a cierto proceso
        print('T: %7.4fs %s: Arm/Trig: Ready >> RAM Request %6.3f' % (env.now, processID, RAM.level))
        # Condicion inicial que juega con las cantidad de instrucciones que llego
        while Inst > 0:
            with CPU.request() as reqCPU: # Pedida al CPU para poder ejecutar dicha instruccion
                yield reqCPU
                print('T: %7.4fs %s: Running instructions %6.3f' % (env.now, processID, Inst))

                yield env.timeout(1)
                # condicion interna con instrucciones para ir terminando las instrucciones en dado caso necesario
                if Inst > 3:
                    Inst = Inst - 3
                else:
                    Inst = 0
            # condicion alterna para verificar la entrada a diferentes modos segun necesidad del proceso
            if Inst > 0:
                nextWait = random.randint(1,2) # Genera el numero aleatorio si metera a modo de espera o terminar la instruccion
                if nextWait == 1: # condicion cuando debe entrar modo de espera segun aleatoriedad
                    with lagTime.request() as reqlagTime: # Pide el tiempo de espera para la instruccion
                        yield reqlagTime 
                        print ('T: %7.4fs %s: Waiting Mode >>' % (env.now, processID))

                        yield env.timeout(1)
                # Instruccion terminado
                print('T: %7.4fs %s: Ready >> Continue >>' % (env.now, processID))
        # Tiempo de proceso en el momento actual
        ProcTime = env.now - arrive
        print ('T: %7.4fs %s: Instruction Terminated, Exe.Time >> %s' % (env.now, processID, ProcTime))
        # Devolucion de RAM despues del uso
        with RAM.put(memoryBlock) as reqReturnRAM:
            yield reqReturnRAM
            print ('T: %7.4fs %s: Freeing used RAM %s' % (env.now, processID, memoryBlock))
        # Calculo de tiempo actual de corridad de simulador
        timeSim = timeSim + (env.now - arrive)
        print('T: %7.4fs Memory Block / RAM Check %6.3f >> Current Time %s' % (env.now, RAM.level, timeSim))        

# Inicia y empieza la simulacion
print('>>SYS. Boot<<')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Ejecutar los procesos
CPU = simpy.Resource(env, capacity=1)
RAM = simpy.Container(env, init=100, capacity=100)
lagTime = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_PROCESS, INTERVAL_PROCESS, RAM, CPU, lagTime))
timeSim = 0
env.run()
print "Tiempo Total de Ejecucion: " , timeSim, ": Promedio del tiempo: " , timeSim/25.0
