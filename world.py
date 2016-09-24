from walls import Column, Wall
from agent import Agent, agent_keys
from time import sleep
from ammo import Bullet, Rocket, Shell
# from exceptions import MapLoadingError
import pygame
from math import pi
from random import random, randint

class World:
    def __init__(self, map_name):
        self.name = map_name
        self.width, self.height = 0, 0
        self.obstacles = []
        self.agents = []
        self.bullets = []
        self.ready = False
        self.background_color = pygame.Color('#101010')
        self.bg = None
        self.time = 0
        self.actions = {'to_go_forward': False,
                        'to_go_back': False,
                        'to_go_left': False,
                        'to_go_right': False,
                        'to_turn_left': False,
                        'to_turn_right': False,
                        'to_shoot': False,
                        'to_take_pistol': False,
                        'to_take_shotgun': False,
                        'to_take_rocket_launcher': False,
                        'to_take_machine_gun': False}

    def load(self):
        map_size, map_agents, map_walls, map_columns = None, None, None, None
        exec('from '+self.name+' import map_size, map_agents, map_walls, map_columns')
        if map_size and map_agents and map_walls and map_columns:
            self.width, self.height = map_size
            self.bg = pygame.Surface(map_size)
            self.bg.fill(self.background_color)

            for params in map_agents:
                agent_creation = 'self.agents.append(Agent('
                for key in agent_keys:
                    agent_creation += "params['"+key+"'],"
                agent_creation = agent_creation[:-1]+'))'
                exec agent_creation
            for col in map_columns:
                self.obstacles.append(Column(col[0], col[1], col[2]))
            for wall in map_walls:
                self.obstacles.append(Wall(wall[0], wall[1], wall[2]))

            self.ready = True
            print 'Loading finished'
        else:
            print 'Loading failed'
            # raise MapLoadingError

    def draw(self, screen):
        screen.blit(self.bg, (0,0))
        for i in self.obstacles:
            i.draw(screen)
        for i in self.agents:
            i.draw(screen)
        for i in self.bullets:
            i.draw(screen)

    def tick(self, player=0):
        self.time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.actions['to_take_pistol'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_1:
                self.actions['to_take_pistol'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.actions['to_take_shotgun'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_2:
                self.actions['to_take_shotgun'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.actions['to_take_rocket_launcher'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_3:
                self.actions['to_take_rocket_launcher'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                self.actions['to_take_machine_gun'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_4:
                self.actions['to_take_machine_gun'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.actions['to_go_forward'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                self.actions['to_go_forward'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.actions['to_go_left'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                self.actions['to_go_left'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.actions['to_go_right'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                self.actions['to_go_right'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.actions['to_go_back'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                self.actions['to_go_back'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.actions['to_turn_left'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_q:
                self.actions['to_turn_left'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.actions['to_turn_right'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                self.actions['to_turn_right'] = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.actions['to_shoot'] = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.actions['to_shoot'] = False
        new_bullets = self.agents[player].update(self.obstacles,
                                                 self.actions['to_go_forward'],
                                                 self.actions['to_go_back'],
                                                 self.actions['to_go_left'],
                                                 self.actions['to_go_right'],
                                                 self.actions['to_turn_left'],
                                                 self.actions['to_turn_right'],
                                                 self.actions['to_shoot'],
                                                 self.actions['to_take_pistol'],
                                                 self.actions['to_take_shotgun'],
                                                 self.actions['to_take_rocket_launcher'],
                                                 self.actions['to_take_machine_gun'])
        self.bullets+=new_bullets
        bullets_to_drop = []
        for i in range(len(self.bullets)):
            self.bullets[i].update(self.obstacles, self.agents)
            if self.bullets[i].exploded:
                bullets_to_drop = [i] + bullets_to_drop
        for i in bullets_to_drop:
            self.bullets = self.bullets[:i] + self.bullets[i+1:]
        sleep(0.01)

