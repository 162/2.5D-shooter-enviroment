import pygame

class Bonus:
    def __init__(self, x, y,
                 new_hp=0,
                 new_armor=0,
                 new_ammo=[0,0,0],
                 radius=3,
                 color='#500000'):
        self.x = x
        self.y = y
        self.new_hp = new_hp
        self.new_armor = new_armor
        self.new_ammo = new_ammo
        self.taken = False
        self.radius = radius
        self.color = pygame.Color(color)

    def distance_to_agent(self, agent):
        return ((self.x-agent.x)**2+(self.y-agent.y)**2)**0.5

    def update(self, agents):
        for i in agents:
            if self.distance_to_agent(i) <= i.radius+self.radius:
                i.take_bonus(self.new_hp, self.new_armor, self.new_ammo)
                self.taken = True

    def draw(self, screen):
        pygame.draw.circle(screen,
                           self.color,
                           (self.x, self.y),
                           self.radius)


class BulletsPack(Bonus):
    def __init__(self, pos):
        Bonus.__init__(self, pos[0], pos[1],
                       new_hp=0,
                       new_armor=0,
                       new_ammo=[10, 0, 0],
                       radius=3,
                       color='#500000')


class ShellsPack(Bonus):
    def __init__(self, pos):
        Bonus.__init__(self, pos[0], pos[1],
                       new_hp=0,
                       new_armor=0,
                       new_ammo=[0, 5, 0],
                       radius=3,
                       color='#500000')


class RocketsPack(Bonus):
    def __init__(self, pos):
        Bonus.__init__(self, pos[0], pos[1],
                       new_hp=0,
                       new_armor=0,
                       new_ammo=[0, 0, 2],
                       radius=3,
                       color='#500000')


class Medkit(Bonus):
    def __init__(self, pos):
        Bonus.__init__(self, pos[0], pos[1],
                       new_hp=50,
                       new_armor=0,
                       new_ammo=[0, 0, 0],
                       radius=5,
                       color='#500000')


class Vest(Bonus):
    def __init__(self, pos):
        Bonus.__init__(self, pos[0], pos[1],
                       new_hp=0,
                       new_armor=50,
                       new_ammo=[0, 0, 0],
                       radius=5,
                       color='#005000')