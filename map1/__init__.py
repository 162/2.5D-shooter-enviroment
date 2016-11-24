map_size = [1080, 720]

# walls color
clr = '#888888'

# walls and columns positions
map_walls = []
map_walls.append(((540, 10), 1080, 20, clr))
map_walls.append(((540, 710), 1080, 20, clr))
map_walls.append(((1070, 360), 20, 720, clr))
map_walls.append(((10, 360), 20, 720, clr))
#for i in range(10, 1080, 20):
#    map_walls.append(((i, 10), 20, 20, clr))
#    map_walls.append(((i, 710), 20, 20, clr))
#for i in range(30, 700, 20):
#    map_walls.append(((10, i), 20, 20, clr))
#    map_walls.append(((1070, i), 20, 20, clr))
map_columns = [((150, 150), 30, clr),
               ((930, 150), 30, clr),
               ((930, 570), 30, clr),
               ((150, 570), 30, clr),
               ((200, 200), 20, clr),
               ((880, 200), 20, clr),
               ((880, 520), 20, clr),
               ((200, 520), 20, clr)]

# Agents generating (without decision functions)
map_agents = [{'max_velocity': 1.2,
               'turn_speed': 0.05,
               'max_health': 100,
               'max_armor': 100,
               'spawn_point': (100, 100),
               'starting_angle': 0,
               'starter_weapon_pack': None,
               'starter_ammo_pack': None,
               'color': '#559955',
               'radius': 12},
              {'max_velocity': 1.2,
               'turn_speed': 0.05,
               'max_health': 100,
               'max_armor': 100,
               'spawn_point': (1000, 100),
               'starting_angle': 0,
               'starter_weapon_pack': None,
               'starter_ammo_pack': None,
               'color': '#555599',
               'radius': 12}]

# Bonuses spawn points with timeouts
map_bonuses = [[(180, 180, 250), (900, 180, 250), (180, 540, 250), (900, 540, 250)],  # bullet packs
               [],  # shells packs
               [],  # rockets packs
               [],  # medkits
               []]  # armor vests
