import json
from classes import Task

def save(tasks, deadline, worker_count, path):
    problem = {
        'tasks': tasks,
        'deadline': deadline,
        'worker_count': worker_count,
    }
    repr = json.dumps(problem)
    with open(path, 'w') as file:
        file.write(repr)

def load(path):
    with open(path, 'r') as file:
        repr = file.read()

    js = json.loads(repr)
    js['tasks'] = list(map(Task.from_json_compatible, js['tasks']))

    return js['tasks'], js['deadline'], js['worker_count']

def generate(task_count, deadline, max_profit):
    from relaxed import generateTasks
    tasks = generateTasks(task_count, deadline, max_profit)
    tasks = list(map(lambda x: x.to_json_compatible(), tasks))
    return tasks

if __name__ == '__main__':
    import sys
    from config import *

    if len(sys.argv) != 2:
        print('ERROR: bad number of arguments.')
        print('Usage: python generate.py path_to_save_to')
        exit()
    path = sys.argv[1]

    tasks = generate(TASK_COUNT, DEADLINE, MAX_PROFIT)
    save(tasks, DEADLINE, WORKER_COUNT, path)   
