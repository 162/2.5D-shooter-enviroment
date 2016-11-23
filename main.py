from world import World
import pygame
from constants import STATS_WIDTH
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
w.agents[0].set_mode('Player')
w.agents[1].set_mode('Target')
w.agents[1].name = 'Target1'

while 1:
    try:
        w.tick()
        w.draw(screen)
        pygame.display.update()
    except:
        profiler.print_stats(sort=1)
        break