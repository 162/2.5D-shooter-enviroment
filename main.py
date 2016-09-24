from world import World
import pygame


w = World(map_name='map1')
w.load()
DISPLAY = (w.width, w.height)
pygame.init()
pygame.display.set_caption(w.name)
myfont = pygame.font.SysFont("timesnewroman", 15)
flags = pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode(DISPLAY, flags)
while 1:
    w.tick()
    w.draw(screen)
    pygame.display.update()