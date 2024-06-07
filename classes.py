from collections import Counter

class Task:
    def __init__(self, time: int, profit: int | float) -> None:
        self.time = time
        self.profit = profit

    def __repr__(self) -> str:
        return f"|{self.time}, {self.profit:.2f}|"

    def to_json_compatible(self):
        return [self.time, self.profit]
    
    @staticmethod
    def from_json_compatible(task):
        return Task(task[0], task[1])

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
