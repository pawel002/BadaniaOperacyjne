import random
import numpy as np

class Task:
    def __init__(self, dealine: int, time: int, profit: int | float) -> None:
        self.deadline = dealine
        self.time = time
        self.profit = profit

    def __repr__(self) -> str:
        return f"D={self.deadline}, T={self.time}, P={self.profit:.2f}"

class Problem:
    def __init__(self, tasks: list[Task], worker_count: int, dealine: int) -> None:
        self.tasks = tasks
        self.worker_count = worker_count
        self.dealine = dealine
        self.solution_matrix = np.array([[[0 for k in range(dealine)] for j in range(len(tasks))] for i in range(worker_count)])

    def __repr__(self) -> str:
        rep = f"{self.worker_count} workers \n {self.dealine} absolute dealine \n {len(tasks)} tasks \n"
        for task in tasks:
            rep += f"{{{task.deadline}, {task.time}, {task.profit:.2f}}}, "
        return rep
    
def generateTasks(count:int, work_dealine: int, maxprofit: int | float) -> list[Task]:
    tasks = []
    for _ in range(count):
        deadline, profit = random.randint(1, work_dealine), random.random() * maxprofit
        time = max(deadline - random.randint(0, deadline), 1)
        tasks.append(Task(deadline, time, profit))

    return tasks

def saveTasks(filename: str, tasks: list[Task]) -> None:
    file = open(filename, 'w')
    file.write('\n'.join([str(t) for t in tasks]))
    file.close()


if __name__ == '__main__':
    tasks = generateTasks(5, 5, 10)
    problem = Problem(tasks, 2, 5)
    print(problem)

