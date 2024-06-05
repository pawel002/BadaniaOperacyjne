from classes import *
import matplotlib.pyplot as plt
import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

font = None

def linearColor(c1, c2, t):
    return tuple([int(x * t + y * (1-t)) for x,y in zip(c1,c2)])

def draw_button(screen, rect, text):
    pygame.draw.rect(screen, BLUE, rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def visualise(instances: list[RelaxedInstance], tasks: list[Task]):
    global font
    
    pygame.init()

    font = pygame.font.SysFont(None, 32)

    pygame.display.set_caption('Visualisation')
    info = pygame.display.Info()
    screen_width = int(info.current_w * 0.95)
    screen_height = int(info.current_h * 0.95)

    screen = pygame.display.set_mode((screen_width, screen_height))

    maxPPT = max([x.profit / x.time for x in tasks])

    clock = pygame.time.Clock()
    deadline = tasks[0].deadline
    instance_idx = 0
    rec_height = screen_height * 0.7 / len(instances[0].task_distrib)

    button_rect = pygame.Rect(0.9 * screen_width, 0.9*screen_height, 200, 100)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    instance_idx += 1

        instance = instances[instance_idx]

        screen.fill(WHITE)

        y = 10
        for _, worker_tasks in enumerate(instance.task_distrib):
            x = 10
            for task_idx in sorted(worker_tasks):
                ppt = (tasks[task_idx].profit / tasks[task_idx].time) / maxPPT
                width = tasks[task_idx].time / deadline * screen_width * 0.95
                c = linearColor(RED, BLUE, ppt)
                pygame.draw.rect(screen, c, (x, y, width, rec_height), 3)
                x += width

            y += rec_height + 5

        pygame.draw.line(screen, (0, 0, 0), (screen_width * 0.95 + 10, 0), (screen_width * 0.95 + 10, y + rec_height), 2)
        draw_button(screen, button_rect, f'{instance_idx}')

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()
