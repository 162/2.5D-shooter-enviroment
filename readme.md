##Environment description

Each tick each agent can perform one or more actions from the list below:

1. to_go_forward
2. to_go_back
3. to_go_left
4. to_go_right
5. to_turn_left
6. to_turn_right
7. to_shoot
8. to_take_pistol
9. to_take_shotgun
10. to_take_rocket_launcher
11. to_take_machine_gun

Some action groups are conflicting. If agent tries to perform conflicting 
actions, neither of them is really performed. For example if agent tries
to go both forward and back it does not move that axis at all.

World expects to receive dictionary of boolean values (keys are set as 
listed above).

Agent has a list of preset attributes:

* max_velocity
* turn_speed
* max_health
* max_armor
* spawn_point
* starting_angle
* starter_weapon_pack - this one is not needed, but it`s scary to delete it
* starter_ammo_pack - this one is not needed, but it`s scary to delete it
* color
* radius

These ones are set by environment before the start of the world.

Agent also has game attributes:

* hp (initial value - max_hp)
* arm (initial value - 0)
* x, y (initial values - spawn_point)
*

...