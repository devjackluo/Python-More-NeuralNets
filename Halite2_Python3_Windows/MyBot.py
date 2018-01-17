
import hlt
import logging
from collections import OrderedDict
from random import randint
import datetime

game = hlt.Game("Settler-working")
logging.info("Starting my Settler bot!")

modnum = 3
raidmode = False


while True:

    a = datetime.datetime.now()

    game_map = game.update_map()
    command_queue = []

    team_ships = game_map.get_me().all_ships()

    planets = game_map.all_planets()

    for ship in team_ships:
        current = 0

        b = datetime.datetime.now()
        delta = b - a
        if int(delta.total_seconds() * 1000) > 1900:
            break

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


        if shipid % modnum == 0:

            if len(closest_enemy_ships) > 0:

                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(ship.closest_point_to(target_ship), game_map,
                                                 speed=int(hlt.constants.MAX_SPEED))
                if navigate_command:
                    command_queue.append(navigate_command)

            elif len(closest_empty_planets) > 0:

                target_planet = closest_empty_planets[0]

                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))
                else:
                    navigate_command = ship.navigate(ship.closest_point_to(target_planet), game_map,
                                                     speed=int(hlt.constants.MAX_SPEED))
                    if navigate_command:
                        command_queue.append(navigate_command)

        else:

            left = (len(game.map.all_planets()) / 2) + (len(game.map.all_planets()) / 5)

            if len(closest_empty_planets) <= left:

                closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if
                                         isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not
                                         entities_by_distance[distance][0].is_full()]

                modnum = 2


            if len(closest_empty_planets) > 0:


                target_planet = closest_empty_planets[0]

                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))
                else:

                    navigate_command = ship.navigate(ship.closest_point_to(closest_empty_planets[current % len(closest_empty_planets)]), game_map, speed=int(hlt.constants.MAX_SPEED))
                        #
                        # navigate_command = ship.navigate(ship.closest_point_to(target_planet), game_map,
                        #                                  speed=int(hlt.constants.MAX_SPEED), ignore_ships=False)
                    if navigate_command:
                        command_queue.append(navigate_command)

            elif len(closest_enemy_ships) > 0:

                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(ship.closest_point_to(target_ship), game_map,
                                                 speed=int(hlt.constants.MAX_SPEED))
                if navigate_command:
                    command_queue.append(navigate_command)


    game.send_command_queue(command_queue)
    # TURN END
