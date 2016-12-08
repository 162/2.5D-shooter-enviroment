from engine.world import World
import pygame
from engine.constants import STATS_WIDTH
import cProfile


profiler = cProfile.Profile()
profiler.enable()

w = World(map_name='map1')
w.load()

DISPLAY = (w.width, w.height)
pygame.init()
pygame.display.set_caption(w.name)
myfont = pygame.font.SysFont("timesnewroman", 15)
flags = pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode(DISPLAY, flags)

# This has to be done somewhere inside world loading
# It`s applying keyboard mode to the only agent

w.agents[0].name = 'BP'
w.agents[1].name = 'Random'
w.agents[2].angle = -1.57
w.agents[2].name = 'Perceptron'
w.agents[3].name = 'DQN'
w.agents[4].name = 'Target1'
w.agents[5].name = 'Target2'
w.agents[6].name = 'Target3'

with open('configs/DQN_default.config', 'r') as f:
    w.agents[3].set_model(f.read())


while 1:
    #try:
    if 1:
        w.tick()
        w.draw(screen)
        pygame.display.update()
    #except:
    #    profiler.print_stats(sort=1)
    #    break