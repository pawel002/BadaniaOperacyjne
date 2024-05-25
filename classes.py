import numpy as np

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
        rep = f"{self.worker_count} workers \n {self.dealine} absolute dealine \n {len(self.tasks)} tasks \n"
        for task in self.tasks:
            rep += f"{str(task)}, "
        return rep
    
class RelaxedInstance:
    def __init__(self, task_distrib) -> None:
        self.task_distrib = task_distrib

    def evaluate(self, tasks: list[Task]):
        profit = 0
        for row in self.task_distrib:
            for task_id in row:
                profit += tasks[task_id].profit

        return profit
    
    def checkValid(self):
        m = Counter([x for row in self.task_distrib for x in row])
        for key in m:
            if m[key] != 1:
                print(f"task {key} has {m[key]} occurances!")
                return False
            
        return True
    
    def __repr__(self) -> str:
        string = ''
        for i, tasks in enumerate(self.task_distrib):
            string += f"Worker {i+1}: {tasks} \n"

        return string