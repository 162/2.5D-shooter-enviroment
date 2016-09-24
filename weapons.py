from random import random
from ammo import *
from constants import *


def draw_pistol(screen, pos, angle):
    for i in range(0, 7, 2):
        x, y = pos[0]+i*cos(angle), pos[1]+i*sin(angle)
        pygame.draw.circle(screen,
                           pygame.Color('#49311c'),
                           (int(x), int(y)),
                           2)


def draw_shotgun(screen, pos, angle):
    for i in range(1, 6, 2):
        x, y = pos[0]+i*cos(angle), pos[1]+i*sin(angle)
        pygame.draw.circle(screen,
                           pygame.Color('#49311c'),
                           (int(x), int(y)),
                           4)
    for i in range(2, 13, 2):
        x, y = pos[0]+i*cos(angle), pos[1]+i*sin(angle)
        pygame.draw.circle(screen,
                           pygame.Color('#222222'),
                           (int(x), int(y)),
                           2)


def draw_rocket_launcher(screen, pos, angle):
    for i in range(4, 13, 2):
        x, y = pos[0]+i*cos(angle), pos[1]+i*sin(angle)
        pygame.draw.circle(screen,
                       pygame.Color('#222222'),
                       (int(x), int(y)),
                       5)
    for i in range(4, 13, 2):
        x, y = pos[0]+i*cos(angle), pos[1]+i*sin(angle)
        pygame.draw.circle(screen,
                           pygame.Color('#555577'),
                           (int(x), int(y)),
                           3)


def draw_machine_gun(screen, pos, angle):
    x, y = pos[0], pos[1]
    pygame.draw.circle(screen,
                       pygame.Color('#662200'),
                       (int(x), int(y)),
                       6)
    for i in range(-1, 10, 2):
        x, y = pos[0]+i*cos(angle), pos[1]+i*sin(angle)
        pygame.draw.circle(screen,
                           pygame.Color('#888800'),
                           (int(x), int(y)),
                           2)


class Weapon:
    def __init__(self, ammo_id, ammo, inaccuracy, per_shot, cooldown, draw_function):
        self.ammo_id = ammo_id
        self.ammo = ammo
        self.cooldown = cooldown
        self.cooling = 0
        self.inaccuracy = inaccuracy
        self.per_shot = per_shot
        self.drawfn = draw_function

    def update(self):
        if self.cooling:
            self.cooling -= 1

    def draw(self, screen, pos, angle):
        self.drawfn(screen, pos, angle)

    def shoot(self, pos, angle):
        if self.cooling:
            return []
        else:
            self.cooling = self.cooldown
            pos = [pos[0]+21*cos(angle), pos[1]+21*sin(angle)]
            return [self.ammo(pos, angle+(random()-random())*self.inaccuracy) for i in range(self.per_shot)]


pistol = Weapon(BULLETS, Bullet, 0.01, 1, 30, draw_pistol)
shotgun = Weapon(SHELLS, Shell, 0.25, 3, 100, draw_shotgun)
rocket_launcher = Weapon(ROCKETS, Rocket, 0.03, 1, 200, draw_rocket_launcher)
machine_gun = Weapon(BULLETS, Bullet, 0.05, 1, 10, draw_machine_gun)