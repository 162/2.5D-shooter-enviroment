map_size = (1080, 720)


clr = '#888888'
map_walls = []
for i in range(10, 1080, 20):
    map_walls.append(((i, 10), 20, clr))
    map_walls.append(((i, 710), 20, clr))
for i in range(30, 700, 20):
    map_walls.append(((10, i), 20, clr))
    map_walls.append(((1070, i), 20, clr))
map_columns = [((150, 150), 30, clr),
               ((930, 150), 30, clr),
               ((930, 570), 30, clr),
               ((150, 570), 30, clr)]
map_agents = [{'max_velocity': 1.2,
               'turn_speed': 0.05,
               'max_health': 100,
               'max_armor': 100,
               'spawn_point': (100, 100),
               'starting_angle': 0,
               'starter_weapon_pack': None,
               'starter_ammo_pack': None,
               'color': '#999999',
               'radius': 12}]
