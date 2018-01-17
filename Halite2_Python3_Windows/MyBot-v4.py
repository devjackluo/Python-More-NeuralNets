import hlt
import logging
from collections import OrderedDict

game = hlt.Game("Settler-vNew")
logging.info("Starting my Settler bot!")

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

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if
                               isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and
                               entities_by_distance[distance][0] not in team_ships]

        closest_occupied_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if
                                 isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and
                                 len(entities_by_distance[distance][0].all_docked_ships()) >= 1]

        if len(game.map.all_planets())/4 <= len(closest_occupied_planets):
            closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if
                                         isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not
                                         entities_by_distance[distance][0].is_full()]
            modnum = 2
        else:
            closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if
                                     isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not
                                     entities_by_distance[distance][0].is_owned()]
            modnum = 3

        if shipid % modnum == 0:

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

    try:
        game.send_command_queue(command_queue)
    except:
        pass