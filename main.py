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

w.agents[1].name = 'Target'
w.agents[2].name = 'Perceptron'

while 1:
    #try:
    if 1:
        w.tick()
        w.draw(screen)
        pygame.display.update()
    #except:
    #    profiler.print_stats(sort=1)
    #    break