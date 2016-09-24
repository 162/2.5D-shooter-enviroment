from constants import *
import pygame
from math import sin, cos, pi
from weapons import pistol, shotgun, rocket_launcher, machine_gun

agent_keys = ['max_velocity',
              'turn_speed',
              'max_health',
              'max_armor',
              'spawn_point',
              'starting_angle',
              'starter_weapon_pack',
              'starter_ammo_pack',
              'color',
              'radius']


class Agent:
    def __init__(self,
                 max_velocity,
                 turn_speed,
                 max_health,
                 max_armor,
                 spawn_point=(200, 200),
                 starting_angle=0,
                 starter_weapon_pack=None,
                 starter_ammo_pack=None,
                 color='#303030',
                 radius=10):

        # name could be added any time
        self.name = 'John'

        # basic stats
        self.max_v = max_velocity
        self.turn_v = turn_speed
        self.max_hp = max_health
        self.max_arm = max_armor

        # current stats
        self.angle = starting_angle
        self.vx, self.vy = 0, 0
        self.v = 0
        self.hp = self.max_hp
        self.arm = 0
        self.x, self.y = spawn_point

        # weaponary
        self.active_weapon = PISTOL
        self.active_ammo = BULLETS
        self.ammo_needed_to_shoot = 1
        self.weapons = [pistol, shotgun, rocket_launcher, machine_gun]
        self.ammo = [10, 5, 1]

        # visualiser options
        self.color = pygame.Color(color)
        self.radius = radius

    def take_damage(self, amount):
        to_armor = min(self.arm, amount/2)
        to_hp = amount - to_armor
        self.arm -= to_armor
        self.hp -= to_hp
        if self.hp <= 0:
            print self.name, 'is dead!'
            raise ValueError

    def draw(self, screen):
        #body
        pygame.draw.circle(screen, self.color,
                           (int(self.x), int(self.y)),
                           self.radius)
        #hands
        pygame.draw.circle(screen, self.color,
                           (int(self.x+self.radius*cos(self.angle+pi/3)),
                            int(self.y+self.radius*sin(self.angle+pi/3))),
                           self.radius/3)
        pygame.draw.circle(screen, self.color,
                           (int(self.x+self.radius*cos(self.angle-pi/3)),
                            int(self.y+self.radius*sin(self.angle-pi/3))),
                           self.radius/3)
        self.weapons[self.active_weapon].draw(screen, pos=(self.x+self.radius*cos(self.angle),
                                                           self.y+self.radius*sin(self.angle)),
                                              angle=self.angle)

    def update(self, obstacles,
               to_go_forward=False, to_go_back=False, to_go_left=False, to_go_right=False,
               to_turn_left=False, to_turn_right=False,
               to_shoot=False,
               to_take_pistol=False,
               to_take_shotgun=False,
               to_take_rocket_launcher=False,
               to_take_machine_gun=False):
        for wpn in self.weapons:
            wpn.update()
        if to_turn_left and not to_turn_right:
            self.angle -= self.turn_v

        if to_turn_right and not to_turn_left:
            self.angle += self.turn_v

        new_x, new_y = self.x, self.y
        if to_go_forward and not to_go_back:
            new_x += self.max_v*cos(self.angle)
            new_y += self.max_v*sin(self.angle)

        if to_go_back and not to_go_forward:
            new_x -= self.max_v*cos(self.angle)/2
            new_y -= self.max_v*sin(self.angle)/2

        if to_go_right and not to_go_left:
            new_x += self.max_v*cos(self.angle+pi/2)/2
            new_y += self.max_v*sin(self.angle+pi/2)/2

        if to_go_left and not to_go_right:
            new_x -= self.max_v*cos(self.angle+pi/2)/2
            new_y -= self.max_v*sin(self.angle+pi/2)/2

        collides = False
        for obs in obstacles:
            if obs.distance_to_point(new_x, new_y) < self.radius:
                collides = True
                break

        if not collides:
            self.x, self.y = new_x, new_y

        if to_take_pistol:
            self.active_weapon = PISTOL
            self.active_ammo = BULLETS
            self.ammo_needed_to_shoot = 1
        if to_take_shotgun:
            self.active_weapon = SHOTGUN
            self.active_ammo = SHELLS
            self.ammo_needed_to_shoot = 5
        if to_take_rocket_launcher:
            self.active_weapon = ROCKET_LAUNCHER
            self.active_ammo = ROCKETS
            self.ammo_needed_to_shoot = 1
        if to_take_machine_gun:
            self.active_weapon = MACHINE_GUN
            self.active_ammo = BULLETS
            self.ammo_needed_to_shoot = 1

        if to_shoot and self.ammo[self.active_ammo]>=self.ammo_needed_to_shoot:
            if self.weapons[self.active_weapon].cooling == 0:
                self.ammo[self.active_ammo] -= self.ammo_needed_to_shoot
            return self.weapons[self.active_weapon].shoot((self.x+self.radius*cos(self.angle),
                                                           self.y+self.radius*sin(self.angle)), angle=self.angle)
        else:
            return []
