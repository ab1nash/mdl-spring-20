from client_moodle import get_errors, submit
import os
import random
import datetime

# of

ar = [-3.063738993688, -3.204337931013725, -6.4434278218704915, 0.058000840738213745,
      0.038118482947526615, 0.00010153485323280556, -6.014152410626804e-05, -1.2458354739067129e-07, 3.4846263904947886e-08, 3.5374495646745877e-11, -6.709685046538829e-12]

kee = 'ewwKbhByHhphaUULhpjpujvwGWsnfzy2lhjgAqsqTDqjN0tNfd'
# Main function


def foo(ar, kee=kee):
    f = open("responses.txt", "a")
    cap = get_errors(kee, ar)
    f.write('Got this!' + str(cap) + ' ' + str(cap[0]+cap[1]))
    f.write(str(ar))
    f.write('\n')
    print(str(cap) + ' ' + str(cap[0]+cap[1]))
    f.close()
    return cap


class Agent:

    def __init__(self, ar):
        self.ar = ar.copy()
        self.fitness = -1


population = 20
generations = 100
# base_val_thr = 1000000.1623710159
# base_train_thr = 1000000.0000000000
# base_val_err = base_val_thr * 2
# base_train_err = base_train_thr * 2
# base_sum_thr = base_val_thr + base_train_thr
# base_sum_err = base_sum_thr * 2


def Genetic_Algorithm():

    # #files for debugging
    # f = open("responses.txt", "a")
    # f2 = open("gendata.txt", "a")

    # f2.write(str(datetime.datetime.now))
    # f.write(str(datetime.datetime.now))
    # f.close()
    # f2.close()
    agents = init_agents(population, ar)
    # for agent in agents:
    #     print(agent.ar)

    for generation in range(generations):

        print('Generation: ' + str(generation))

        agents = fitness(agents)
        # for agent in agents:
        #     print(agent.fitness)
        agents = selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)
        # agents = mutation(agents)
        # agents = mutation(agents)
        print(submit(kee, agents[0].ar))
        # gen after gen
        # f2 = open("gendata.txt", "a")
        # for agent in agents:
        #     f2.write(str(agent.ar) + '\n fitness for #' +
        #              str(agents.index(agent)) + 'is ' + str(agent.fitness))
        #     f2.write('\n')

        # f2.write(
        #     '\n---------------------------------------------------------------\n' + str(generation))

        # f2.close()
        # f = open("responses.txt", "a")
        # f.write(
        #     '\niter is:----------------------------------------------------------------\n' + str(generation))
        # f.close()

    # Cutoff for coarse
        # if any(agent.fitness > 900 for agent in agents):
        #     print('Threshold reached!')
        # exit(0)


def init_agents(population, ar):

    ret = [Agent(ar) for _ in range(population)]
    for a in ret:
        k = random.randint(1, 10)
        l = random.randint(1, 10)
        a.ar[k] += random.uniform(-a.ar[k] *
                                  0.0000001, a.ar[k]*0.0000001)
        a.ar[l] += random.uniform(-a.ar[l] *
                                  0.0000001, a.ar[l]*0.0000001)

    # trace = open("trace.txt", "a")
    # trace.write('INIT:\n')
    # for ag in ret:
    #     trace.write(str(ag.ar) + '\n')
    # trace.close()
    return ret


def fitness(agents):
    # maxer = 0
    for agent in agents:
        cap = foo(agent.ar)
        train = cap[0]
        val = cap[1]

        bve = 0 * val**4
        bte = 0 * train**4
        thr = 1000 * (val+train)**5

        agent.fitness = 0 * \
            (1-(abs(val-train)/max(val, train))) + bve + bte + thr
        # if(agent.fitness < -1):
        #     agent.fitness = -1
        # if(train > base_train_thr or val > base_val_thr or thr > base_sum_thr):
        # agent.fitness = -2
        # if(thr > base_sum_thr):
        #     agent.fitness = -2

    return agents


def selection(agents):

    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=False)

    agents = agents[:int(0.8*len(agents))]

    return agents


def crossover(agents):

    # randomly recombine parts of 2
    offspring = []

    # Make children according to population
    for _ in range(0, int(population/10)):
        parent1 = Agent(ar)
        parent2 = Agent(ar)

        yy = random.choice(
            list(filter(lambda agent: agent.fitness > 0, agents)))
        # yy = agents[0]
        parent1.ar = yy.ar.copy()
        allowed_values = agents.copy()
        allowed_values.remove(yy)
        parent2.ar = random.choice(
            list(filter(lambda agent: agent.fitness > 0, allowed_values))).ar.copy()

        # trace = open("trace.txt", "a")
        # trace.write('\nVectors selected for crossover:\n')
        # trace.write(str(parent1.ar) + '\n' + str(parent2.ar))
        # trace.close()

        child1 = Agent(ar)
        child2 = Agent(ar)

        # Can/May change this
        child1.ar = parent1.ar.copy()
        for idx in range(0, len(parent2.ar)):
            if random.uniform(0.0, 1.0) < 0.6:
                child1.ar[idx] = parent2.ar[idx]

        child2.ar = parent2.ar.copy()
        for idx in range(0, len(parent1.ar)):
            if random.uniform(0.0, 1.0) < 0.6:
                child2.ar[idx] = parent1.ar[idx]

        offspring.append(child1)
        offspring.append(child2)

    # trace = open("trace.txt", "a")
    # trace.write('\nVectors produced after crossover:\n')
    # trace.write(str(child1.ar) + '\n' + str(child2.ar))
    # trace.close()

    agents.extend(offspring)

    return agents


def mutation(agents):

    # modify this
    erval = 0.0000000000000008

    # trace = open("trace.txt", "a")
    # trace.write('\nVectors before mutation:\n')
    # for agent in agents:
    #     trace.write(str(agent.ar) + '\n')
    # trace.close()

    for agent in agents:

        for idx in range(0, len(agent.ar)):
            # for _ in range(0, 1):
            # idx = random.randint(0, len(agent.ar)-1)

            if random.uniform(0.0, 1.0) <= 0.5:
                new_ar = []

                for idd in range(0, idx):
                    new_ar.append(agent.ar[idd])

                new_ar.append(agent.ar[idx] +
                              random.uniform(-erval, erval))
                for idd in range(idx+1, len(agent.ar)):
                    new_ar.append(agent.ar[idd])

                agent.ar = new_ar.copy()
                # print('mutationsuccess')

    # trace = open("trace.txt", "a")
    # trace.write('\nVectors after mutation:\n')
    # for agent in agents:
    #     trace.write(str(agent.ar) + '\n')
    # trace.close()

    return agents


# Running the code
Genetic_Algorithm()

# END
