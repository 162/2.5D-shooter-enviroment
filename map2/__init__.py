map_size = [540, 370]

# walls color
clr = '#888888'

# walls and columns positions
map_walls = []
map_walls.append(((270, 10), 540, 20, clr))
map_walls.append(((270, 360), 540, 20, clr))
map_walls.append(((530, 190), 20, 370, clr))
map_walls.append(((10, 190), 20, 370, clr))

map_columns = [((0, 0), 30, clr)]
               #((200, 200), 20, clr),
               #((880, 200), 20, clr),
               #((880, 520), 20, clr),
               #((200, 520), 20, clr)]


default_parameters = {'max_velocity': 1.2,
                      'turn_speed': 0.05,
                      'max_health': 100,
                      'max_armor': 100,
                      'spawn_point': (130, 50),
                      'starting_angle': 0,
                      'starter_weapon_pack': None,
                      'starter_ammo_pack': None,
                      'color': '#4444dd',
                      'radius': 12}

# Agents generating (without decision functions)
map_agents = [('DQNAgent', default_parameters.copy()),
              ('EmptyAgent', default_parameters.copy()),
              ('EmptyAgent', default_parameters.copy()),
              ('EmptyAgent', default_parameters.copy()),
              ('EmptyAgent', default_parameters.copy())]


map_agents[1][1]['color'] = '#555555'
map_agents[1][1]['spawn_point'] = (420, 80)

map_agents[4][1]['color'] = '#555555'
map_agents[4][1]['spawn_point'] = (180, 280)


map_agents[2][1]['color'] = '#555555'
map_agents[2][1]['spawn_point'] = (380, 230)


map_agents[3][1]['color'] = '#555555'
map_agents[3][1]['spawn_point'] = (380, 80)



# Bonuses spawn points with timeouts
map_bonuses = [[], [], [], [], []]
