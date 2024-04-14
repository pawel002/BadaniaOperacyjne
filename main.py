import random
import numpy as np
import copy

class Task:
    def __init__(self, dealine: int, time: int, profit: int | float) -> None:
        self.deadline = dealine
        self.time = time
        self.profit = profit

    def __repr__(self) -> str:
        return f"|{self.deadline}, {self.time}, {self.profit:.2f}|"

class Problem:
    def __init__(self, tasks: list[Task], worker_count: int, deadline: int) -> None:
        self.tasks = tasks
        self.worker_count = worker_count
        self.deadline = deadline
        self.used_problems = [False for _ in range(len(tasks))]
        self.solution_matrix = np.zeros((worker_count, len(tasks), deadline))
        self.profit = 0

    def __repr__(self) -> str:
        rep = f"{self.worker_count} workers \n {self.dealine} absolute dealine \n {len(tasks)} tasks \n"
        for task in tasks:
            rep += f"{str(task)}, "
        return rep
    
def generateTasks(count:int, work_dealine: int, maxprofit: int | float) -> list[Task]:
    tasks = []
    for _ in range(count):
        deadline, profit = random.randint(1, work_dealine), random.random() * maxprofit
        time = max(deadline - random.randint(0, deadline), 1)
        tasks.append(Task(deadline, time, profit))

    return tasks

def generateRandom(tasks: list[Task], worker_count: int, deadline: int, worker_tries: int) -> Problem:
    '''
    Generates random solution. For each task it tries to fit it randomly into any worker's timeline ``worker_tries`` times.
    Upon failure of fitting task, skips to next task.
    '''

    problem = Problem(tasks, worker_count, deadline)
    matrix = problem.solution_matrix
    workers_timeline = np.zeros((worker_count, deadline))

    # for each task
    for task_idx, task in enumerate(tasks):
        
        # generate random start time for each task in the interval <0, deadline - time> and try to fit it into any agent
        for worker in range(worker_count):

            break_worker = False
            
            # how many times we will try to fit the task to each worker
            for _ in range(worker_tries):
                
                # select random time
                start = random.randint(0, task.deadline - task.time)
                can_fit_task = True

                # if worker is busy during this time
                if np.any(workers_timeline[worker, start : start + task.time]):
                    can_fit_task = False

                # if we can fit this task
                if can_fit_task:

                    problem.used_problems[task_idx] = True
                    workers_timeline[worker, start : start + task.time] = 1
                    matrix[worker, task_idx, start] = 1
                    break_worker = True
                    problem.profit += task.profit

                    break

            # if we managed to fit the task we can go to next task
            if break_worker:
                break
    
    return problem

def generateBasedOnMaxPay(tasks: list[Task], worker_count: int, deadline: int):
    '''
    First sort the tasks using ``task.pay / task.time`` metric. After that iterate over tasks and
    try to fit the task to any worker starting from <dealine - time, deadline> and going down to
    <deadline - time - 1, deadline - 1> and so on.
    '''

    tasks.sort(key=lambda x: x.profit/x.time, reverse=True)

    problem = Problem(tasks, worker_count, deadline)
    matrix = problem.solution_matrix
    workers_timeline = np.zeros((worker_count, deadline))

    for task_idx, task in enumerate(tasks):

        for worker in range(worker_count):

            break_worker = False
            start = task.deadline - task.time

            while start >= 0:

                # if the worker is busy try to fit it earlier
                if np.any(workers_timeline[worker][start : start + task.time]):
                    start -= 1
                    continue

                workers_timeline[worker][start : start + task.time] = 1
                problem.used_problems[task_idx] = True
                matrix[worker, task_idx, start] = 1
                problem.profit += task.profit
                break_worker = True

                break

            
            if break_worker:
                break
    
    return problem

def checkSolution(problem: Problem):
    
    # check if the task is assigned only once
    for i in range(len(problem.tasks)):
        if not 0 <= np.sum(problem.solution_matrix[:, i, :]) <= 1:
            print("Failed at: Check 1")
            return False
        
    # check if the the task is assigned before its deadline
    for i in range(len(problem.tasks)):
        for j in range(problem.worker_count):

            idx = np.where(problem.solution_matrix[j, i] == 1)
            if len(idx[0]) >= 1:
                time_start = idx[0][0]
                if time_start + problem.tasks[i].time > problem.tasks[i].deadline:
                    print("Failed at: Check 2")
                    return False
                
    # for each worker check if any tasks overlap
    for j in range(problem.worker_count):
        helper_matrix = problem.solution_matrix[j].T

        i = 0
        while i < helper_matrix.shape[0]:

            idx = np.where(helper_matrix[i] == 1)
            if len(idx[0]) == 1:
                task_idx = idx[0][0]
                execution_time = problem.tasks[task_idx].time

                j = 1
                while j < execution_time:
                    if np.sum(helper_matrix[i + j]) >= 1:
                        print("Failed at: Check 3")
                        return False
                    
                    j += 1

                i += j

            i += 1

    return True

def saveTasks(filename: str, tasks: list[Task]) -> None:
    file = open(filename, 'w')
    file.write('\n'.join([str(t).replace(",", "").replace("|", "") for t in tasks]))
    file.close()

def loadTasks(filename: str) -> list[Task]:
    file = open(filename, 'r')
    tasks = []
    for line in file.readlines():
        parsed = list(map(float, line.split(" ")))
        tasks.append(Task(int(parsed[0]), int(parsed[1]), parsed[2]))

    return tasks

if __name__ == '__main__':
    random.seed(42)
    test_directory = "tests/"

    day_deadline = 10
    workers = 5
    tasks = generateTasks(20, day_deadline, 10)

    problem = generateBasedOnMaxPay(copy.deepcopy(tasks), workers, day_deadline)
    print(checkSolution(problem))
    print(problem.profit)

    problem = generateRandom(copy.deepcopy(tasks), workers, day_deadline, 10)
    print(checkSolution(problem))
    print(problem.profit)

