import random
import copy
import numpy as np
from classes import *
from visualize import *
        
def generateTasks(count: int, work_deadline: int, maxprofit: int | float) -> list[Task]:
    tasks = []
    for _ in range(count):
        profit = round(random.random() * maxprofit, 2)
        time = max(random.randint(0, work_deadline), 1)
        tasks.append(Task(time, profit))

    return tasks

def generateRandomSolution(tasks: list[Task], worker_count: int, deadline: int):
    task_distrib = [[] for _ in range(worker_count)] # t_d[i] = tasks for i-th worker
    worker_times = [0 for _ in range(worker_count)]
    unused_tasks = [i for i in range(len(tasks))]
    profit = 0

    gen = list(enumerate(tasks))
    random.shuffle(gen)

    for task_id, task in gen:
        for i in range(worker_count):
            if worker_times[i] + task.time <= deadline:
                worker_times[i] += task.time
                task_distrib[i].append(task_id)
                profit += task.profit
                unused_tasks.remove(task_id)
                break

        if sum(worker_times) == worker_count * deadline:
            break

    return task_distrib, profit, unused_tasks

def genetic_func(instance1: RelaxedInstance, instance2: RelaxedInstance, 
                 tasks: list[Task], deadline: int):

    worker_count = len(instance1.task_distrib)
    worker_perm = [i for i in range(worker_count)]

    def fit(time, instance, task_idx):

        for worker_idx in worker_perm:

            if time[worker_idx] + tasks[task_idx].time <= deadline:
                time[worker_idx] += tasks[task_idx].time
                instance[worker_idx].append(task_idx)
                return True
            
        return False

    used1 = [i for row in instance1.task_distrib for i in row]
    used2 = [i for row in instance2.task_distrib for i in row]

    mark_used = [0 for _ in range(len(tasks))]

    new_instance1 = [[] for _ in range(worker_count)]
    worker_time1 = [0 for _ in range(worker_count)]
    
    new_instance2 = [[] for _ in range(worker_count)]
    worker_time2 = [0 for _ in range(worker_count)]

    for task_set in [used1, used2]:
        for task_idx in task_set:

            random.shuffle(worker_perm)
            if mark_used[task_idx] == 1:

                fit(worker_time2, new_instance2, task_idx)
                continue

            if mark_used[task_idx] == 2:

                fit(worker_time1, new_instance1, task_idx)
                continue

            if random.random() < 0.5:
                
                if fit(worker_time1, new_instance1, task_idx):
                    mark_used[task_idx] = 1
                    continue
                
                fit(worker_time2, new_instance2, task_idx)

            else:
                
                if fit(worker_time2, new_instance2, task_idx):
                    mark_used[task_idx] = 2
                    continue

                fit(worker_time1, new_instance1, task_idx)

    return RelaxedInstance(new_instance1), RelaxedInstance(new_instance2)

def mutate(instance: RelaxedInstance, tasks: list[Task],
           deadline: int, pop_prob: float):

    worker_count = len(instance.task_distrib)
    worker_perm = [i for i in range(worker_count)]
    new_instance = [[x for x in row if random.random() < pop_prob] for row in instance.task_distrib]
    worker_time = [sum([tasks[i].time for i in row]) for row in new_instance]
    random.shuffle(worker_perm)

    def fit(time, instance, task_idx):

        for worker_idx in worker_perm:

            if time[worker_idx] + tasks[task_idx].time <= deadline:
                time[worker_idx] += tasks[task_idx].time
                instance[worker_idx].append(task_idx)
                return True
            
        return False


    used = set(i for row in new_instance for i in row)
    unused = set(range(len(tasks))) - used
    unused_profit = [(tasks[i].profit / tasks[i].time, i) for i in unused]
    unused_profit.sort(reverse=True)
    # random.shuffle(unused_profit)

    for _, task_id in unused_profit:

        fit(worker_time, new_instance, task_id)
        random.shuffle(worker_perm)

    return RelaxedInstance(new_instance)

def evolutionAlg(population: list[RelaxedInstance], tasks: list[Task], 
                 deadline: int, iterations: int, mutation_prob: float, 
                 quiet: bool=False, plot: bool=True):
    
    population_size = len(population)
    population.sort(key=lambda x: x.evaluate(tasks), reverse=True)
    best_instance, best_profit = None, 0
    average, best = [], []

    instances = []

    for iter_count in range(iterations):

        for population_idx in range(0, len(population), 2):
            
            i1, i2 = population[population_idx], population[population_idx + 1]
            new_i1, new_i2 = genetic_func(i1, i2, tasks, deadline)

            if random.random() < mutation_prob:
                population.append(mutate(new_i1, tasks, deadline, 0.25))

            if random.random() < mutation_prob:
                population.append(mutate(new_i2, tasks, deadline, 0.25))
   
            population.append(new_i1)
            population.append(new_i2)

        population.sort(key=lambda x: x.evaluate(tasks), reverse=True)
        population = population[:population_size]

        population_evaluation = np.average(np.array([x.evaluate(tasks) for x in population]))
        cur_best, cur_best_ev = population[0], population[0].evaluate(tasks)

        if cur_best_ev > best_profit:
            best_profit = cur_best_ev
            best_instance = cur_best

        if plot:
            average.append(population_evaluation)
            best.append(best_profit)
        instances.append(copy.deepcopy(best_instance))

        if not quiet:
            print(f"{iter_count} ITERATION. \n      average = {population_evaluation:.2f} \n      curbest = {cur_best_ev:.2f} \n      alltime = {best_profit:.2f}")


    if plot:
        plot_dict = {
            'x_values' : [i for i in range(len(best))],
            'average' : average,
            'best' : best,
        }
        return best_instance, instances, plot_dict
    else:
        return best_instance, instances, {}

def evolution(population, tasks, deadline):
    
    # remove random parts from solution
    population = copy.deepcopy(population)
    for solution_idx, (task_distribution, unassigned_tasks) in enumerate(population):
        removed = copy.deepcopy(unassigned_tasks)
        for worker_tasks in range(len(task_distribution)):
            to_remove = []
            for task in task_distribution[worker_tasks]:
                if random.random() > 0.5:
                    to_remove.append(task)
            
            for task_to_remove in to_remove:
                task_distribution[worker_tasks].remove(task_to_remove)
                removed.append(task_to_remove)


        # apply removed parts back into the solution
        idx = 0
        max_iter = 1000
        while idx < max_iter:
            if len(removed) == 0:
                break
            removed_id = removed[idx % len(removed)]
            selected_worker = random.randint(0, len(task_distribution) - 1)
            
            current_time = 0
            for task_id in task_distribution[selected_worker]:
               current_time += tasks[task_id].time 

            if tasks[removed_id].time + current_time <= deadline:
                task_distribution[selected_worker].append(removed_id)
                removed.remove(removed_id)

            idx += 1

        population[solution_idx] = task_distribution, -1, removed

    return population

from config import MUTATION_PROB, PATH, PLOT
def run(algorithm, from_path = PATH, to_plot = PLOT, override_wc = False):
    """ 
    algorithm -> 1 - Basic Evolutionary Algorithm,
                 2 - Traditional Genetic Algorithm,
                 3 - Both;
    from_path -> False - generates new instance of problem based on the config file
              -> 'some_path' - assuming 'some_path' leads to a json file generated
                 using the generate.py module, then it loads that instance of a problem
    """
    assert algorithm == 1 or algorithm == 2 or algorithm == 3, "Error: algorithm <- {1, 2, 3}"
    from config import DEADLINE, TASK_COUNT, MAX_PROFIT, WORKER_COUNT, \
                       BASE_POPULATION_SIZE, MAX_ITER
    from time import perf_counter
    DEADLINE_true = DEADLINE
    WORKER_COUNT_true = WORKER_COUNT
    tasks = []
    if from_path == False:
        tasks = generateTasks(TASK_COUNT, DEADLINE, MAX_PROFIT)
    else:
        from generate import load
        tasks, DEADLINE_true, WORKER_COUNT_true = load(from_path)
    
    if override_wc:
        WORKER_COUNT_true = override_wc

    population = []
    base_population = []
    for _ in range(BASE_POPULATION_SIZE):
        task_distrib, _, removed = generateRandomSolution(tasks, WORKER_COUNT_true, DEADLINE_true)
        population.append(RelaxedInstance(task_distrib))
        base_population.append((task_distrib, removed))

    f_profit, s_profit = 0, 0
    f_time, s_time = 0, 0
    if algorithm == 1 or algorithm == 3:
        s = perf_counter()
        best_profit = 0
        # best_distribution = base_population[0]
        profit_list = []
        best_profit_list = []
        curr_best_list = []
        
        for _ in range(MAX_ITER):
            current_population = evolution(base_population, tasks, DEADLINE_true)

            current_profit = 0
            for current_solution in current_population:
                current_profit = calculate_profit_from_distribution(current_solution[0], tasks)

                if current_profit > best_profit:
                    best_profit = current_profit
                    # best_distribution = current_solution[0]

            if to_plot:
                profit_list.append(np.mean(np.array(list(map(lambda x: calculate_profit_from_distribution(x[0], tasks), current_population)))))
                curr_best_list.append(np.max(np.array(list(map(lambda x: calculate_profit_from_distribution(x[0], tasks), current_population)))))
            best_profit_list.append(best_profit)

        f_time = perf_counter() - s
        f_profit = best_profit_list[-1]

        if to_plot:
            x_values = list(range(len(profit_list)))
            plt.title(label="Basic evolutionary algorithm")
            plt.plot(x_values, profit_list, label="Average Population Profit")
            plt.plot(x_values, best_profit_list, label="Best Profit So Far")
            plt.plot(x_values, curr_best_list, label="Best Population Profit")
            plt.xlabel("Iteration")
            plt.ylabel("Profit")
            plt.legend()
            plt.show()
        print('--------------------------------')
        print('Basic Evolutionary Algorithm:')
        print(f'\tprofit = {f_profit:.2f}')
        print(f'\ttime   = {f_time:.2f} s.')

    if algorithm == 2 or algorithm == 3:
        from config import MUTATION_PROB 
        s = perf_counter()
        best, all_instances, plot_data = evolutionAlg(population, tasks, DEADLINE_true, 
                                           MAX_ITER, MUTATION_PROB, quiet=True, plot=to_plot)
        s_time = perf_counter() - s
        s_profit = best.evaluate(tasks)

        if to_plot:
            plot_end(plot_data, "Traditional Genetic Algorithm")
        print('Traditional Genetic Algorithm:')
        print(f'\tprofit = {s_profit:.2f}')
        print(f'\ttime   = {s_time:.2f} s.')

    return (f_profit, f_time), (s_profit, s_time)

def calculate_profit_from_distribution(task_distribution, tasks):
    profit = 0
    for worker_tasks in task_distribution:
        for task in worker_tasks:
            profit += tasks[task].profit

    return profit
