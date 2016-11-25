from base_agent import BaseAgent
import pygame
from keras.layers import Input, Dense, Flatten
from keras.models import Model
from keras.optimizers import RMSprop
import numpy as np
from random import random

actions_list = ['to_go_forward', 'to_go_back', 'to_go_left', 'to_go_right',
                'to_turn_left', 'to_turn_right', 'to_shoot', 'to_take_pistol',
                'to_take_shotgun', 'to_take_rocket_launcher', 'to_take_machine_gun']


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


class PerceptronAgent(BaseAgent):
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
        input_layer = Input(shape=(8, 17))
        flattened_input = Flatten()(input_layer)
        inner_layer = Dense(20, activation='relu')(flattened_input)
        output_layer = Dense(11, activation='tanh')(inner_layer)
        self.model = Model(input_layer, output_layer)
        self.model.compile(RMSprop(),
                           loss='hinge')
        self.delta = 1-1e-6
        self.epsilon = 1

    def think(self, observation):
        global actions_list
        observation = np.array(observation)
        try:
            r = random()
            if r < self.epsilon:
                actions = [random()**2 > 0.95 for i in range(11)]
            else:
                observation = observation.reshape((1, 8, 17))
                pred = self.model.predict(observation)
                actions = [i > 0 for i in pred[0]]
            self.actions = {actions_list[i]: actions[i] for i in range(11)}
            self.epsilon *= self.delta
        except:
            pass

    def observe(self, observation, reward):
        global actions_list
        observation = np.array(observation)
        try:
            observation = observation.reshape((1, 8, 17))
            actions = np.array([int(self.actions[i])*reward for i in actions_list])
            actions = actions.reshape((1, 11))
            self.model.fit(observation, actions, nb_epoch=1, verbose=0)
        except:
            pass





