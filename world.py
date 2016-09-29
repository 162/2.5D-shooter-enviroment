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
        self.bonus_spawner = []

    def load(self):
        map_size, map_agents, map_walls, map_columns, map_bonuses = None, None, None, None, None
        exec('from '+self.name+' import map_size, map_agents, map_walls, map_columns, map_bonuses')
        if map_size and map_agents and map_walls and map_columns and map_bonuses:
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

            for i in range(len(all_bonuses)):
                for bonus in map_bonuses[i]:
                    self.bonus_spawner.append({'self': all_bonuses[i],
                                               'pos': (bonus[0], bonus[1]),
                                               'cooldown': bonus[2],
                                               'spawn_next_in': bonus[2]})

            self.ready = True
            print 'Loading finished'
        else:
            print 'Loading failed'
            # raise MapLoadingError

    def draw(self, screen):
        screen.blit(self.bg, (0,0))
        for i in self.obstacles:
            i.draw(screen)
        for i in self.bonuses:
            i.draw(screen)
        for i in self.agents:
            i.draw(screen)
        for i in self.bullets:
            i.draw(screen)

    def tick(self, player=0):
        self.time += 1

        for bonus in self.bonus_spawner:
            if bonus['spawn_next_in'] > 1:
                bonus['spawn_next_in'] -= 1
            elif bonus['spawn_next_in'] == 1:
                self.bonuses.append(bonus['self'](bonus['pos']))
                bonus['spawn_next_in'] = 0
            elif bonus['spawn_next_in'] == 0:
                taken = True
                for i in self.bonuses:
                    if i.x == bonus['pos'][0] and i.y == bonus['pos'][1]:
                        taken = False
                        break
                if taken:
                    bonus['spawn_next_in'] = bonus['cooldown']

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

