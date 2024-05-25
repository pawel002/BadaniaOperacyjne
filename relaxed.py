import random
import copy
from classes import *
import matplotlib.pyplot as plt

class RelaxedInstance:
    def __init__(self, task_distrib) -> None:
        self.task_distrib = task_distrib

    def evaluate(self, tasks: list[Task]):
        profit = 0
        for row in self.task_distrib:
            for task_id in row:
                profit += tasks[task_id].profit

        return profit
        

def generateTasks(count: int, work_dealine: int, maxprofit: int | float) -> list[Task]:
    tasks = []
    for _ in range(count):
        profit = random.random() * maxprofit
        time = max(random.randint(0, work_dealine), 1)
        tasks.append(Task(work_dealine, time, profit))

    return tasks

def generateRandomSolution(tasks: list[Task], worker_count: int):
    deadline = tasks[0].deadline # same for every task
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

def genetic_func(instance1: RelaxedInstance, instance2: RelaxedInstance, tasks: list[Task]):

    worker_count = len(instance1.task_distrib)
    deadline = tasks[0].deadline
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
    worker_time1 = [0 for i in range(worker_count)]
    
    new_instance2 = [[] for _ in range(worker_count)]
    worker_time2 = [0 for i in range(worker_count)]

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
                    continue
                
                fit(worker_time2, new_instance2, task_idx)

            else:
                
                if fit(worker_time2, new_instance2, task_idx):
                    continue

                fit(worker_time1, new_instance1, task_idx)

    return RelaxedInstance(new_instance1), RelaxedInstance(new_instance2)

def mutate(instance: RelaxedInstance, tasks: list[Task], pop_prob: float):

    worker_count = len(instance.task_distrib)
    deadline = tasks[0].deadline
    worker_perm = [i for i in range(worker_count)]
    new_instance = [[x for x in row if random.random() < pop_prob] for row in instance.task_distrib]
    worker_time = [sum([tasks[i].profit for i in row]) for row in new_instance]

    def fit(time, instance, task_idx):

        for worker_idx in worker_perm:

            if time[worker_idx] + tasks[task_idx].time <= deadline:
                time[worker_idx] += tasks[task_idx].time
                instance[worker_idx].append(task_idx)
                return True
            
        return False


    used = set(i for row in new_instance for i in row)
    unused = set(range(len(tasks))) - used
    unused_profit = [(tasks[i].profit, i) for i in unused]
    unused_profit.sort(reverse=True)

    for _, task_id in unused_profit:

        fit(worker_time, new_instance, task_id)

    return RelaxedInstance(new_instance)

def evolutionAlg(population: list[RelaxedInstance], tasks: list[Task], iterations: int, mutation_prob: float):
    
    population_size = len(population)
    population.sort(key=lambda x: x.evaluate(tasks), reverse=True)
    best_instance, best_profit = None, 0
    average, best, pop_best, pop_worst = [], [], [], []

    instances = []

    for iter_count in range(iterations):

        for population_idx in range(0, len(population), 2):
            
            i1, i2 = population[population_idx], population[population_idx + 1]
            new_i1, new_i2 = genetic_func(i1, i2, tasks)

            if random.random() < mutation_prob:
                population.append(mutate(new_i1, tasks, 0.25))

            if random.random() < mutation_prob:
                population.append(mutate(new_i2, tasks, 0.25))
   
            population.append(new_i1)
            population.append(new_i2)

        population.sort(key=lambda x: x.evaluate(tasks), reverse=True)
        population = population[:population_size]

        population_evaluation = np.average(np.array([x.evaluate(tasks) for x in population]))
        cur_best, cur_best_ev = population[0], population[0].evaluate(tasks)

        if cur_best_ev > best_profit:
            best_profit = cur_best_ev
            best_instance = cur_best

        average.append(population_evaluation)
        best.append(best_profit)
        pop_best.append(cur_best_ev)
        pop_worst.append(population[-1].evaluate(tasks))
        instances.append(copy.deepcopy(best_instance))

        print(f"{iter_count} ITERATION. \n      average = {population_evaluation:.2f} \n      curbest = {cur_best_ev:.2f} \n      alltime = {best_profit:.2f}")

        if population_evaluation >= best_profit * 0.99999:
            break

    x_values = [i for i in range(len(best))]
    plt.plot(x_values, average, label="Average population profit")
    plt.plot(x_values, best, label="Best Profit")
    plt.scatter(x_values, pop_best, label="Best Profit For Population", s=0.1)
    plt.scatter(x_values, pop_worst, label="Worst Profit For Population", s=0.1)
    plt.xlabel("Iteration")
    plt.ylabel("Profit Score")
    plt.legend()
    plt.show()

    return best_instance, instances

def evolution(population, tasks, deadline):
    
    # remove random parts from solution
    population = copy.deepcopy(population)
    for solution_idx, (task_distribution, profit, unassigned_tasks) in enumerate(population):
        distribution_copy = copy.deepcopy(task_distribution)
        unassigned_copy = copy.deepcopy(unassigned_tasks)
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

def calculate_profit_from_distribution(task_distribution, tasks):
    profit = 0
    for worker_tasks in task_distribution:
        for task in worker_tasks:
            profit += tasks[task].profit

    return profit

def visualise(instances: list[RelaxedInstance]):
    # jak sie komus chce to moze sprobowac
    pass

if __name__ == "__main__":

    random.seed(42)
    np.random.seed(42)

    BASE_POPULATION_SIZE = 40
    WORKER_COUNT = 10
    DEADLINE = 50
    TASK_COUNT = 500
    MAX_ITER = 200
    DEBUG_LOG = False 

    tasks = generateTasks(TASK_COUNT, DEADLINE, 10)

    random.seed(123)
    np.random.seed(42134)

    population = []
    for _ in range(BASE_POPULATION_SIZE):
        task_distrib, _, _ = generateRandomSolution(tasks, WORKER_COUNT)
        population.append(RelaxedInstance(task_distrib))

    best, all_instances = evolutionAlg(population, tasks, MAX_ITER, 0.2)
    # visualise(all_instances)


