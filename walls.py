import pygame


class Column:
    def __init__(self, center_pos, radius=25, color='#303030'):
        self.radius = radius
        self.x, self.y = center_pos
        self.color = pygame.Color(color)

    def draw(self, screen):
        pygame.draw.circle(screen,
                           self.color,
                           (self.x, self.y),
                           self.radius)

    def distance_to_point(self, x, y):
        return ((self.x-x)**2 + (self.y-y)**2)**0.5 - self.radius


class Wall:
    def __init__(self, center_pos, radius=25, color='#303030'):
        self.radius = radius
        self.x, self.y = center_pos
        self.rect = pygame.Rect(self.x-radius, self.y-radius,
                                2*radius, 2*radius)
        self.color = pygame.Color(color)

    def draw(self, screen):
        pygame.draw.rect(screen,
                         self.color,
                         self.rect)

    def distance_to_point(self, x, y):
        min_dist = 10000
        for d in [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]:
            dist = ((self.x+d[0]*self.radius-x)**2 + (self.y+d[1]*self.radius-y)**2)**0.5
            if dist < min_dist:
                min_dist = dist
        return min_dist
