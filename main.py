from engine.world import World
import pygame
from engine.constants import STATS_WIDTH
import cProfile


profiler = cProfile.Profile()
profiler.enable()

w = World(map_name='map_duel')
w.load()

DISPLAY = (w.width, w.height)
pygame.init()
pygame.display.set_caption(w.name)
myfont = pygame.font.SysFont("timesnewroman", 15)
flags = pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode(DISPLAY, flags)

# This has to be done somewhere inside world loading
# It`s applying keyboard mode to the only agent

w.agents[0].name = '2700'
#w.agents[1].name = '1100'
#w.agents[2].name = '1600'
w.agents[1].name = 'Random'

w.agents[0].load('saved/DQN52753.h5')
w.agents[0].to_learn = True
w.agents[0].epsilon = 0.3
w.agents[0].delta = 1-5e-6
w.agents[0].skip = 5
#w.agents[1].load('saved/DQN51100.h5')
#w.agents[1].to_learn = False
#w.agents[1].epsilon = 0.05
#w.agents[2].load('saved/DQN51600.h5')
#w.agents[2].to_learn = False
#w.agents[2].epsilon = 0.05

while 1:
    #try:
    if 1:
        w.tick()
        w.draw(screen)
        pygame.display.update()
    #except:
    #    profiler.print_stats(sort=1)
    #    break