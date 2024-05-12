import random
import copy
from classes import *

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
    profit = 0

    for task_id, task in enumerate(tasks):
        for i in range(worker_count):
            if worker_times[i] + task.time <= dealine:
                worker_times[i] += task.time
                task_distrib[i].append(task_id)
                profit += task.profit         
                break

    for i in range(worker_count):
        print(f"time = {worker_times[i]}")
        print(*task_distrib[i])

    return task_distrib, profit

def evolutionAlg1(population, tasks):
    # implement lol
    pass


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
        
    tasks = generateTasks(20, 10, 10)
    task_distribution, profit = generateRandomSolution(tasks, 3)
    print(profit)

