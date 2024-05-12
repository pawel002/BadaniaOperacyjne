import random
import copy
from classes import *
import matplotlib.pyplot as plt

def generateTasks(count: int, work_dealine: int, maxprofit: int | float) -> list[Task]:
    tasks = []
    for _ in range(count):
        profit = random.random() * maxprofit
        time = max(random.randint(0, work_dealine), 1)
        tasks.append(Task(work_dealine, time, profit))

    return tasks

def generateRandomSolution(tasks: list[Task], worker_count: int):
    dealine = tasks[0].deadline # same for every task
    task_distrib = [[] for _ in range(worker_count)] # t_d[i] = tasks for i-th worker
    worker_times = [0 for _ in range(worker_count)]
    unused_tasks = [i for i in range(len(tasks))]
    profit = 0

    for task_id, task in enumerate(tasks):
        for i in range(worker_count):
            if worker_times[i] + task.time <= dealine:
                worker_times[i] += task.time
                task_distrib[i].append(task_id)
                profit += task.profit
                unused_tasks.remove(task_id)
                break

    for i in range(worker_count):
        print(f"time = {worker_times[i]}")
        print(*task_distrib[i])

    return task_distrib, profit, unused_tasks

def evolutionAlg1(population,  tasks):
    # implement lol
    pass


def evolution(population, tasks, deadline):
    
    # remove random parts from solution
    old_population = copy.deepcopy(population)
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


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    BASE_POPULATION_SIZE = 10
    WORKER_COUNT = 3
    DEADLINE = 10
    MAX_ITER = 500

    DEBUG_LOG = True 
        
    tasks = generateTasks(20, DEADLINE, 10)
    # task_distribution, profit = generateRandomSolution(tasks, WORKER_COUNT)
    base_population = []
    for _ in range(BASE_POPULATION_SIZE):
        base_population.append(generateRandomSolution(tasks, WORKER_COUNT))

    print(*base_population)
    print('-'*15)

    best_profit = 0
    best_distribution = base_population[0]
    profit_list = []
    best_profit_list = []

    for iter in range(MAX_ITER):
        current_population = evolution(base_population, tasks, DEADLINE)

        for current_solution in current_population:
            current_profit = calculate_profit_from_distribution(current_solution[0], tasks)

            if current_profit > best_profit:
                best_profit = current_profit
                best_distribution = current_solution[0]


            print(f"Current best profit:\n{best_profit}")
            if DEBUG_LOG:
                print('-'*20)
                print(f"Current iter:\n{iter}")
                print(f"Current profit:\n {current_profit}")
                # print(f"Population: {current_population}")

        profit_list.append(current_profit)
        best_profit_list.append(best_profit)

    x_values = [i for i in range(len(profit_list))]
    plt.plot(x_values, profit_list, label="Current Profit")
    plt.plot(x_values, best_profit_list, label="Current Best Profit")
    plt.xlabel("Iteration")
    plt.ylabel("Profit Score")
    plt.show()
    print(*best_distribution)

