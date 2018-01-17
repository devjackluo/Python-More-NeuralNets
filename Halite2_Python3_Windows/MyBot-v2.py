
import hlt
import logging
from collections import OrderedDict

game = hlt.Game("Settler-V2")
logging.info("Starting my Settler bot!")

planned_planets = []
count = 0
moving = []

while True:

    game_map = game.update_map()
    command_queue = []

    team_ships = game_map.get_me().all_ships()


    for ship in team_ships:

        shipid = ship.id

        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if
                                 isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not
                                 entities_by_distance[distance][0].is_owned()]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if
                               isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and
                               entities_by_distance[distance][0] not in team_ships]



        if shipid % 3 == 0:

            if len(closest_enemy_ships) > 0:

                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(ship.closest_point_to(target_ship), game_map,
                                                 speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)

            elif len(closest_empty_planets) > 0:

                target_planet = closest_empty_planets[0]

                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))
                else:
                    navigate_command = ship.navigate(ship.closest_point_to(target_planet), game_map,
                                                     speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                    if navigate_command:
                        command_queue.append(navigate_command)

        else:


            if len(closest_empty_planets) > 0:

                target_planet = closest_empty_planets[0]

                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))
                else:
                    navigate_command = ship.navigate(ship.closest_point_to(target_planet), game_map, speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                    if navigate_command:
                        command_queue.append(navigate_command)

            elif len(closest_enemy_ships) > 0:

                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(ship.closest_point_to(target_ship), game_map,
                                                 speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)





    game.send_command_queue(command_queue)
    # TURN END


# # GAME END



#
#         for planet in game_map.all_planets():
#
#             # If the planet is owned
#             if planet.is_owned():
#                 # Skip this planet
#                 continue
#
#             # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
#             if ship.can_dock(planet):
#                 # We add the command by appending it to the command_queue
#                 command_queue.append(ship.dock(planet))
#             else:
#
#                 if planet in planned_planets:
#                     continue
#                 else:
#                     # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
#                     # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
#                     # We run this navigate command each turn until we arrive to get the latest move.
#                     # Here we move at half our maximum speed to better control the ships
#                     # In order to execute faster we also choose to ignore ship collision calculations during navigation.
#                     # This will mean that you have a higher probability of crashing into ships, but it also means you will
#                     # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
#                     # wish to turn that option off.
#                     navigate_command = ship.navigate(
#                         ship.closest_point_to(planet),
#                         game_map,
#                         speed=int(hlt.constants.MAX_SPEED),
#                         ignore_ships=True)
#                     # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
#                     # or we are trapped (or we reached our destination!), navigate_command will return null;
#                     # don't fret though, we can run the command again the next turn)
#                     if navigate_command:
#                         command_queue.append(navigate_command)
#                         planned_planets.append(planet)
#
#             break
#
#     # Send our set of commands to the Halite engine for this turn
#     game.send_command_queue(command_queue)
#     # TURN END
# # GAME END
