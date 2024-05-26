from relaxed import generateTasks, generateRandomSolution, RelaxedInstance, evolution, evolutionAlg
from relaxed import visualise

def perform_tests() -> None:
    
    TEST_LENGTH = 3
    SEEDS = [42, 57, 85]
    POPULATIONS = [20,40,60]
    WORKERS = [5,10,20]
    DEADLINE = 50
    TASK_COUNT = [250, 500, 750]
    MAX_ITER = [100,200,400]

    for test in range(TEST_LENGTH):
        tasks = generateTasks(TASK_COUNT[test], DEADLINE, 10)
        population = []
        for _ in range(POPULATIONS[test]):
            task_distrib, _, _ = generateRandomSolution(tasks, WORKERS[test])
            population.append(RelaxedInstance(task_distrib))
    
    best, all_instances = evolutionAlg(population, tasks, MAX_ITER[test], 0.2)
    # visualise(all_instances, tasks)

if  __name__ == "__main__":

    perform_tests()