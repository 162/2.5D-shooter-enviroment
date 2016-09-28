from walls import Column, Wall
from agent import Agent, agent_keys
from time import sleep
from ammo import Bullet, Rocket, Shell
from bonuses import *
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
        self.bonuses = []
        self.ready = False
        self.background_color = pygame.Color('#101010')
        self.bg = None
        self.time = 0

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
        for i in self.bonuses:
            i.draw(screen)

    def tick(self, player=0):
        self.time += 1
        if self.time % 100 == 1:
            self.bonuses.append(RocketsPack((randint(300, 600), randint(200, 400))))
        self.agents[player].think()
        new_bullets = self.agents[player].update(self.obstacles)
        self.bullets += new_bullets
        bullets_to_drop = []
        for i in range(len(self.bullets)):
            self.bullets[i].update(self.obstacles, self.agents)
            if self.bullets[i].exploded:
                bullets_to_drop = [i] + bullets_to_drop
        for i in bullets_to_drop:
            self.bullets = self.bullets[:i] + self.bullets[i+1:]

        bonuses_to_drop = []
        for i in range(len(self.bonuses)):
            self.bonuses[i].update(self.agents)
            if self.bonuses[i].taken:
                bonuses_to_drop = [i] + bonuses_to_drop
        for i in bonuses_to_drop:
            self.bonuses = self.bonuses[:i] + self.bonuses[i+1:]
        sleep(0.01)

