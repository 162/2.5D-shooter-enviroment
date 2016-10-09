from walls import Column, Wall
from agent import Agent, agent_keys
from time import sleep
from bonuses import *
# from exceptions import MapLoadingError
import pygame
from math import pi
from random import random, randint
from time import time
from constants import *


journal = []


stats_names = ['Pos', 'Name', 'K', 'D', 'K-D', 'K/D', 'HP', 'A', 'B', 'S', 'R']


def render_line(screen, lst, x0, y0):
    deltas = [0, 32, 80, 24, 24, 32, 40, 32, 32, 32, 32]
    text_color = pygame.Color('#ffffff')
    bg_color = pygame.Color('#101010')
    font = pygame.font.SysFont('timesnewroman', 16)
    for i in range(len(lst)):
        header = font.render(str(lst[i]), True, text_color, bg_color)
        screen.blit(header, (x0+sum(deltas[:i+1]), y0))


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
        self.stats_bg = None
        self.time = 0
        self.bonus_spawner = []
        self.stats = []

    def load(self):
        map_size, map_agents, map_walls, map_columns, map_bonuses = None, None, None, None, None
        exec('from '+self.name+' import map_size, map_agents, map_walls, map_columns, map_bonuses')
        if map_size and map_agents and map_walls and map_columns and map_bonuses:
            map_size[0]+=STATS_WIDTH
            self.width, self.height = map_size
            self.bg = pygame.Surface((self.width-STATS_WIDTH, self.height))
            self.bg.fill(self.background_color)
            self.stats_bg = pygame.Surface((STATS_WIDTH, self.height))
            self.stats_bg.fill(self.background_color)

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

            self.fill_holder()

            self.ready = True
            print 'Loading finished'
        else:
            print 'Loading failed'
            # raise MapLoadingError

    def fill_holder(self):
        self.stats = []
        for agent in self.agents:
            kdr = 1.0
            if agent.deaths:
                kdr = float(agent.kills)/agent.deaths
            line = [1,
                    agent.name,
                    agent.kills,
                    agent.deaths,
                    agent.kills-agent.deaths,
                    kdr,
                    agent.hp,
                    agent.arm,
                    agent.ammo[BULLETS],
                    agent.ammo[SHELLS],
                    agent.ammo[ROCKETS]]
            self.stats.append(line)

    def draw_stats(self, screen):
        global stats_names
        x0, y0 = self.width-STATS_WIDTH, 0
        columns_pos = []
        screen.blit(self.stats_bg, (x0, y0))
        render_line(screen, stats_names, x0, y0)
        pos = 1
        self.stats.sort(key=lambda x: -x[STAT_SCORE])
        for agent_stats in self.stats:
            agent_stats[0] = pos
            render_line(screen, agent_stats, x0, y0+16*pos)
            pos += 1

    def draw(self, screen):
        screen.blit(self.bg, (0,0))
        for i in self.obstacles:
            i.draw(screen)
        for i in self.bonuses:
            i.draw(screen)
        for i in self.agents:
            if i.is_alive:
                i.draw(screen)
        for i in self.bullets:
            i.draw(screen)
        self.draw_stats(screen)

    def tick(self):
        start = time()
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

        killers = []
        for agent in self.agents:
            if agent.is_alive:
                agent.think()
                new_bullets = agent.update(self.obstacles)
                self.bullets += new_bullets
            elif agent.to_resurrect:
                agent.to_resurrect -= 1
                if agent.killed_by:
                    killers.append(agent.killed_by)
                    agent.killed_by = 0
            else:
                agent.reset()

        for i in killers:
            self.agents[i-1].kills+=1

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

        self.fill_holder()

        frame_time = 1.0/FPS
        time_taken = time()-start
        if time_taken < frame_time:
            sleep(frame_time-time_taken)
        else:
            print time_taken

