from classes import *
import matplotlib.pyplot as plt
import pygame
import sys

def visualise(instances: list[RelaxedInstance], tasks: list[Task]):

    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Visualisation')

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()
    deadline = tasks[0].deadline
    instance_idx = 0

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        instance = instances[instance_idx]

        screen.fill(WHITE)


        y = 10
        rec_height = 20
        for i, worker_tasks in enumerate(instance.task_distrib):
            x = 10
            for task_idx in worker_tasks:
                width = int(tasks[task_idx].time / 50 * 750)
                pygame.draw.rect(screen, BLUE, (x, y, width, rec_height), 2)
                x += width

            y += rec_height + 5

        pygame.draw.line(screen, (0, 0, 0), (760, 0), (760, y + rec_height), 2)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

