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

w.agents[0].name = 'P4'
w.agents[1].name = 'Random'
#w.agents[6].name = 'P2'
w.agents[3].name = 'DQN5'
w.agents[4].name = 'Target1'
w.agents[5].name = 'Target2'
w.agents[2].name = 'Target3'
#w.agents[7].name = 'DQN4'
#w.agents[8].name = 'DQN3'
#w.agents[9].name = 'DQN4'


with open('configs/P4.conf', 'r') as f:
    w.agents[0].set_model(f.read())
#with open('configs/P2.conf', 'r') as f:
#    w.agents[6].set_model(f.read())
with open('configs/DQN5.conf', 'r') as f:
    w.agents[3].set_model(f.read())
#with open('configs/DQN4.conf', 'r') as f:
#    w.agents[7].set_model(f.read())
#with open('configs/DQN3.conf', 'r') as f:
#    w.agents[8].set_model(f.read())
#with open('configs/DQN4.conf', 'r') as f:
#    w.agents[9].set_model(f.read())

while 1:
    #try:
    if 1:
        w.tick()
        w.draw(screen)
        pygame.display.update()
    #except:
    #    profiler.print_stats(sort=1)
    #    break