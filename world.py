from walls import Column, Wall
from agent import Agent, agent_keys
from time import sleep
from bonuses import *
# from exceptions import MapLoadingError
import pygame
from math import pi, sin, cos
from random import random, randint
from time import time
from constants import *
import numpy as np


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

        self.angle_shift = 0.125
        self.rays = 17
        self.critical_distance = 5
        self.layers = 8
        self.vision_range = 100
        self.distance_shift = 10

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

    def get_all_collisions(self, x, y, r, ai, walls_, enemies_, bonus_medkits_, bonus_vests_,
                           bonus_bullets_, bonus_shells_, bonus_rockets_, flying_bullets_):
        s = time()
        collisions = [False]*8
        walls = [i.distance_to_point(x, y)<r for i in walls_]
        if walls:
            collisions[OBSTACLES_LAYER] = max(walls)
        enemies = [i.distance_to_point(x, y)<r for i in enemies_]
        if enemies:
            collisions[ENEMIES_LAYER] = max(enemies)
        bonus_medkits = [i.distance_to_point(x, y)<r for i in bonus_medkits_]
        if bonus_medkits:
            collisions[MEDKITS_LAYER] = max(bonus_medkits)
        bonus_vests = [i.distance_to_point(x, y)<r for i in bonus_vests_]
        if bonus_vests:
            collisions[VESTS_LAYER] = max(bonus_vests)
        bonus_bullets = [i.distance_to_point(x, y)<r for i in bonus_bullets_]
        if bonus_bullets:
            collisions[BULLETS_LAYER] = max(bonus_bullets)
        bonus_shells = [i.distance_to_point(x, y)<r for i in bonus_shells_]
        if bonus_shells:
            collisions[SHELLS_LAYER] = max(bonus_shells)
        bonus_rockets = [i.distance_to_point(x, y)<r for i in bonus_rockets_]
        if bonus_rockets:
            collisions[ROCKETS_LAYER] = max(bonus_rockets)
        flying_bullets = [i.distance_to_point(x, y)<r for i in flying_bullets_]
        if flying_bullets:
            collisions[MISSILES_LAYER] = max(flying_bullets)
        journal.append(time()-s)
        return collisions

    def get_observation(self, agent_index):
        x0 = self.agents[agent_index].x
        y0 = self.agents[agent_index].y
        a0 = self.agents[agent_index].angle

        angles = np.arange(-1, 1.01, self.angle_shift)
        observation = np.zeros(shape=(self.layers, self.rays))

        walls_ = [(i.distance_to_point(x0, y0)<2*self.vision_range) for i in self.obstacles]
        walls = []
        for i in range(len(walls_)):
            if walls_[i]:
                walls.append(self.obstacles[i])

        enemies_ = [(i.id!=self.agents[agent_index].id and i.is_alive) for i in self.agents]
        enemies = []
        for i in range(len(enemies_)):
            if enemies_[i]:
                enemies.append(self.agents[i])
        bonus_medkits_ = [(i.new_hp>0) for i in self.bonuses]
        bonus_medkits = []
        for i in range(len(bonus_medkits_)):
            if bonus_medkits_[i]:
                bonus_medkits.append(self.bonuses[i])
        bonus_vests_ = [(i.new_armor>0) for i in self.bonuses]
        bonus_vests = []
        for i in range(len(bonus_vests_)):
            if bonus_vests_[i]:
                bonus_vests.append(self.bonuses[i])
        bonus_bullets_ = [(i.new_ammo[BULLETS]>0) for i in self.bonuses]
        bonus_bullets = []
        for i in range(len(bonus_bullets_)):
            if bonus_bullets_[i]:
                bonus_bullets.append(self.bonuses[i])
        bonus_shells_ = [(i.new_ammo[SHELLS]>0) for i in self.bonuses]
        bonus_shells = []
        for i in range(len(bonus_shells_)):
            if bonus_shells_[i]:
                bonus_shells.append(self.bonuses[i])
        bonus_rockets_ = [(i.new_ammo[ROCKETS]>0) for i in self.bonuses]
        bonus_rockets = []
        for i in range(len(bonus_rockets_)):
            if bonus_rockets_[i]:
                bonus_rockets.append(self.bonuses[i])
        flying_bullets_ = [(i.owner_id!=self.agents[agent_index].id) for i in self.bullets]
        flying_bullets = []
        for i in range(len(flying_bullets_)):
            if flying_bullets_[i]:
                flying_bullets.append(self.bullets[i])

        for a in range(self.rays):
            for d in range(1, self.vision_range/self.distance_shift):
                px, py = x0+d*self.distance_shift*cos(a0+angles[a]), y0+d*self.distance_shift*sin(a0+angles[a])
                collisions = self.get_all_collisions(px, py, self.critical_distance, self.agents[agent_index].id, walls,
                                                     enemies, bonus_medkits, bonus_vests, bonus_bullets,
                                                     bonus_shells, bonus_rockets, flying_bullets)
                for i in range(self.layers):
                    if collisions[i] and observation[i][a]==0:
                        observation[i][a] = float(self.vision_range-d*self.distance_shift)/self.vision_range
                if collisions[0]:
                    break
        return observation

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
        i = 0
        for agent in self.agents:
            if agent.is_alive:
                obs = self.get_observation(i)
                agent.think(obs)
                new_bullets = agent.update(self.obstacles)
                self.bullets += new_bullets
            elif agent.to_resurrect:
                agent.to_resurrect -= 1
                if agent.killed_by:
                    killers.append(agent.killed_by)
                    agent.killed_by = 0
            else:
                agent.reset()
            i += 1

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
            print time_taken, sum(journal)/len(journal)

