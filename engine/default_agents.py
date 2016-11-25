from base_agent import BaseAgent
import pygame


class KeyboardAgent(BaseAgent):
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
        BaseAgent.__init__(self,
                           max_velocity,
                           turn_speed,
                           max_health,
                           max_armor,
                           spawn_point,
                           starting_angle,
                           starter_weapon_pack,
                           starter_ammo_pack,
                           color,
                           radius)

    def think(self, observation):
        #actions = {}
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
        return self.actions

    def observe(self, observation, reward):
        pass


class EmptyAgent(BaseAgent):
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
        BaseAgent.__init__(self,
                           max_velocity,
                           turn_speed,
                           max_health,
                           max_armor,
                           spawn_point,
                           starting_angle,
                           starter_weapon_pack,
                           starter_ammo_pack,
                           color,
                           radius)
