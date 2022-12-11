"""
This is the missionarys and cannibals game logic
"""


import sys
import pygame


def game():
    def ferry(passengers, step, position):
        """
        This function is in charge of move sprites("passengers")(taking the
        center by refference) to the final position.
        The passengers[0] is the leader and the reference.
        All the other sprites will move in the same direction than the leader.
        Each time is called 1 step is moved.
        In case that one step is higher than the distance between passenger[0]
        center and position, the passenger is directly move to the position.
        If the passenger leader is in position when steps movement are finished
        the sprite will look in the oposite direction.

        If the passenger[0] is in the final position at the end
        return true if not return false.
        """
        position = (int(position[0]), int(position[1]))
        done = False
        who = []
        for passenger in passengers:
            if passenger is not None:
                who.append(passenger)
        leader = who[0]

        dist_to_goal_x = leader["rect"].centerx - position[0]
        dist_to_goal_y = leader["rect"].centery - position[1]

        if position[0] != leader["rect"].centerx:
            if (abs(dist_to_goal_x) < step):
                if (-1 <= abs(dist_to_goal_x) <= 1):
                    for actor in who:
                        actor["rect"].centerx = position[0]
                else:
                    for actor in who:
                        actor["rect"] = actor["rect"].move(
                            (-dist_to_goal_x, 0))
            elif (leader["rect"].centerx - position[0]) >= 0:
                for actor in who:
                    actor["rect"] = actor["rect"].move((-step, 0))
            else:
                for actor in who:
                    actor["rect"] = actor["rect"].move((step, 0))

        if position[1] != leader["rect"].centery:
            if (abs(dist_to_goal_y) < step):
                if (-1 <= abs(dist_to_goal_y) <= 1):
                    for actor in who:
                        actor["rect"].centery = position[1]
                else:
                    for actor in who:
                        actor["rect"] = actor["rect"].move((0, dist_to_goal_y))
            elif (leader["rect"].centery - position[1]) >= 0:
                for actor in who:
                    actor["rect"] = actor["rect"].move((0, -step))
            else:
                for actor in who:
                    actor["rect"] = actor["rect"].move((0, step))

        if position == leader["rect"].center:
            for actor in who:
                actor["surf"] = pygame.transform.flip(
                    actor["surf"], True, False)
            done = True

        return done

    def freePos(who):
        """
        It realease the space that is ocuppied by who
        on the sides (Not in the boat)
        Spaces are stored in left_places and right_places
        """
        for space in left_places:
            if space[1] is not None:
                if space[1]["id"] == who["id"]:
                    space[1] = None
                    break

        for space in right_places:
            if space[1] is not None:
                if space[1]["id"] == who["id"]:
                    space[1] = None
                    break

    def foundPosition(who):
        """
        It returns "right" if "who" is in right_places
        It returns "left" if "who" is in lenft_places
        """
        for position in right_places:
            if position[1] is not None:
                if position[1]["id"] == who["id"]:
                    return "right"
        for position in left_places:
            if position[1] is not None:
                if position[1]["id"] == who["id"]:
                    return "left"

    def freeBoatPos(who):
        """
        It release the space that is occupied by who
        in the boat
        """
        nonlocal boat_place1
        nonlocal boat_place2
        if boat_place1["id"] == who["id"]:
            boat_place1 = {"id": "void"}
            boat_passengers[1] = None

        if boat_place2["id"] == who["id"]:
            boat_place2 = {"id": "void"}
            boat_place2["id"] = "void"
            boat_passengers[2] = None

    def mountBoat(who, boat, position):
        """
        It mounts "who" into "boat" "position"
        """
        boat_long = boat["rect"].right - boat["rect"].left
        if position == 1:
            done = ferry([who],
                         step,
                         (boat["rect"].left + (boat_long / 4 * 1),
                          boat["rect"].centery - height * 0.1))
            if done:
                freePos(who)
            return done
        else:
            done = ferry([who],
                         step,
                         (boat["rect"].left + (boat_long / 4 * 3),
                          boat["rect"].centery - height * 0.1))
            if done:
                freePos(who)
            return done

    def dismount(who):
        """
        It moves "who" from the "boat" to the corresponding
        place in the sides of the river.
        It uses the funcion ferry()
        """
        if boatPlace == "right":
            for i, space in enumerate(right_places):

                # If space is not occuppied
                if space[1] is None:
                    # We move "who" to the space
                    # and if movement is finished
                    if (ferry([who], step, (space[0]))):
                        # We occuppied the space
                        space[1] = who
                        # printLibreSpaces()
                        freeBoatPos(who)
                        # The movement is finished
                        return True
                    # The space is being reached, so we don't
                    # want to search for more spaces
                    break

        elif boatPlace == "left":
            for i, space in enumerate(left_places):
                # If space is not occuppied
                if space[1] is None:
                    # We move "who" to the space
                    # and if movement is finished
                    if (ferry([who], step, (space[0]))):
                        # We occuppied the space
                        space[1] = who
                        # printLibreSpaces()
                        freeBoatPos(who)
                        # The movement is finished
                        return True
                    # The space is being reached, so we don't
                    # want to search for more spaces
                    break

        # The movement is not finished
        return False

    def printLibreSpaces():
        """
        It prints the libre spaces of the boat.
        This function is only used for debug.
        """
        print("\n\n")
        for i, place in enumerate(left_places):
            if place[1] is None:
                print(f"Left: {i}, {place[0]},0")
            else:
                print(f"Left: {i}, {place[0]}, Ocupied")

        print("\n\n")
        for i, place in enumerate(right_places):
            if place[1] is None:
                print(f"Right: {i}, {place[0]}, 0")
            else:
                print(f"Right: {i}, {place[0]}, Ocupied")

    def gameState():
        """
        It returns the game for example "-R-mmmccc"
        """
        gamestate = ""
        missionaries = 0
        canibals = 0
        for place in left_places:
            if place[1] is not None:
                if place[1]["type"] == "canibal":
                    canibals += 1
                if place[1]["type"] == "missionarie":
                    missionaries += 1

        if boatPlace == "left":
            if boat_passengers[1] is not None:
                if boat_passengers[1]["type"] == "canibal":
                    canibals += 1
                if boat_passengers[1]["type"] == "missionarie":
                    missionaries += 1
            if boat_passengers[2] is not None:
                if boat_passengers[2]["type"] == "missionarie":
                    missionaries += 1
                if boat_passengers[2]["type"] == "canibal":
                    canibals += 1

        for i in range(missionaries):
            gamestate += "m"
        for i in range(canibals):
            gamestate += "c"

        if boatPlace == "right":
            gamestate += "-R-"
        else:
            gamestate += "-L-"

        missionaries = 0
        canibals = 0

        for place in right_places:
            if place[1] is not None:
                if place[1]["type"] == "canibal":
                    canibals += 1
                if place[1]["type"] == "missionarie":
                    missionaries += 1

        if boatPlace == "right":
            if boat_passengers[1] is not None:
                if boat_passengers[1]["type"] == "canibal":
                    canibals += 1
                if boat_passengers[1]["type"] == "missionarie":
                    missionaries += 1
            if boat_passengers[2] is not None:
                if boat_passengers[2]["type"] == "missionarie":
                    missionaries += 1
                if boat_passengers[2]["type"] == "canibal":
                    canibals += 1

        for i in range(missionaries):
            gamestate += "m"
        for i in range(canibals):
            gamestate += "c"

        return gamestate

    def updateSpacesStatus(last_movement_object):
        """
        It update the last_movement_object in a logical way
        For example if it was in left_places and now is into
        the boat. This function remove it from left_spaces
        """
        movement_id = last_movement_object["id"]
        completed = False
        for place in left_places:
            if place[1] is not None and place[1]["id"] == movement_id:
                place[1] = last_movement_object
                completed = True
                break

        if not completed:
            for place in right_places:
                if place[1] is not None and place[1]["id"] == movement_id:
                    place[1] = last_movement_object
                    break

    def eventListener():
        """
        If an actor is clicked it returns it
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, actor in enumerate(actors):
                    if actor["rect"].collidepoint(mouse_pos):
                        return actor
        else:
            return

    pygame.init()

    width = 800
    height = 480
    white = (255, 255, 255)
    black = (0, 0, 0)

    window = pygame.display.set_mode((width, height))
    screen_rect = window.get_rect()
    landscape = pygame.image.load("images/landscape2.jpg").convert()
    landscape = pygame.transform.scale(landscape, (width, height))

    boat_place1 = {"id": "void"}
    boat_place2 = {"id": "void"}

    missionarie1 = {
        "file": "images/baby.png",
        "id": "missionarie1",
        "type": "missionarie"}
    missionarie2 = {
        "file": "images/baby.png",
        "id": "missionarie2",
        "type": "missionarie"}
    missionarie3 = {
        "file": "images/baby.png",
        "id": "missionarie3",
        "type": "missionarie"}

    cannibal1 = {
        "file": "images/cannibal.png",
        "id": "cannibal1",
        "type": "canibal"}
    cannibal2 = {
        "file": "images/cannibal.png",
        "id": "cannibal2",
        "type": "canibal"}
    cannibal3 = {
        "file": "images/cannibal.png",
        "id": "cannibal3",
        "type": "canibal"}

    boatLeftSide = (screen_rect.width / 7 * 2, screen_rect.centery)
    boatRightSide = (screen_rect.width / 7 * 5, screen_rect.centery)
    boat = {"id": "boat"}
    boat["surf"] = pygame.image.load("images/boat.png")
    boat["surf"] = pygame.transform.scale(
        boat["surf"], (screen_rect.width / 4, screen_rect.height / 4))
    boat["rect"] = boat["surf"].get_rect()
    boat["rect"].center = boatLeftSide

    actors = [
        missionarie1,
        missionarie2,
        missionarie3,
        cannibal1,
        cannibal2,
        cannibal3]

    gamegraph = {
        "mmmccc-L-": {"mm": "mccc-R-mm", "cc": "mmmc-R-cc", "m": "mmccc-R-m",
                      "c": "mmmcc-R-c", "mc": "mmcc-R-mc"},
        "mccc-R-mm": "fail",
        "mmmc-R-cc": {"cc": "mmmccc-L-", "c": "mmmcc-L-c"},
        "mmmcc-L-c": {"mm": "mcc-R-mmc", "cc": "mmm-R-ccc", "m": "mmcc-R-mc",
                      "c": "mmmc-R-cc", "mc": "mmc-R-mcc"},
        "mcc-R-mmc": "fail",
        "mmm-R-ccc": {"cc": "mmmcc-L-c", "c": "mmmc-L-cc"},
        "mmmc-L-cc": {"mm": "mc-R-mmcc", "m": "mmc-R-mcc",
                      "c": "mmm-R-ccc", "mc": "mm-R-mccc"},
        "mc-R-mmcc": {"mm": "mmmc-L-cc", "cc": "mccc-L-mm",
                      "m": "mmc-L-mcc", "c": "mcc-L-mmc", "mc": "mmcc-L-mc"},
        "mmcc-L-mc": {"mm": "cc-R-mmmc", "cc": "mm-R-mccc",
                      "m": "mcc-R-mmc", "c": "mmc-R-mcc", "mc": "mc-R-mmcc"},
        "cc-R-mmmc": {"mm": "mmcc-L-mc", "m": "mcc-L-mmc",
                      "c": "ccc-L-mmm", "mc": "mccc-L-mm"},
        "ccc-L-mmm": {"cc": "c-R-mmmcc", "c": "cc-R-mmmc"},
        "c-R-mmmcc": {"mm": "mmc-L-mcc", "cc": "ccc-L-mmm",
                      "m": "mc-L-mmcc", "c": "cc-L-mmmc", "mc": "mcc-L-mmc"},
        "mc-L-mmcc": {"m": "c-R-mmmcc", "c": "m-R-mmccc", "mc": "-R-mmmccc"},
        "m-R-mmccc": {"mm": "mmm-L-ccc", "cc": "mcc-L-mmc", "m": "mm-L-mccc",
                      "c": "mc-L-mmcc", "mc": "mmc-L-mcc"},
        "-R-mmmccc": "success",
        "cc-L-mmmc": {"cc": "-R-mmmccc", "c": "c-R-mmmcc"},
        "mcc-L-mmc": "fail",
        "mmc-L-mcc": "fail",
        "mccc-L-mm": "fail",
        "mm-R-mccc": "fail",
        "mmc-R-mcc": "fail",
        "mmccc-R-m": {"m": "mmmccc-L-"},
        "mmmcc-R-c": {"c": "mmmccc-L-"},
        "mmcc-R-mc": {"m": "mmmcc-L-c", "c": "mmccc-L-m", "mc": "mmmccc-L-"},
        "mmccc-L-m": {"mm": "ccc-R-mmm", "cc": "mmc-R-mcc", "m": "mccc-R-mm",
                      "c": "mmcc-R-mc", "mc": "mcc-R-mmc"},
        "ccc-R-mmm": {"mm": "mmccc-L-m", "m": "mmmc-L-cc"}}

    right_places = []
    left_places = []
    for i in right_places:
        i[0] = i[0] + (screen_rect.height / 100)
    for i in right_places:
        i[0] = i[0] + (screen_rect.height / 100)

    for i, actor in enumerate(actors):
        size_actor = screen_rect.height / 8
        actor["surf"] = pygame.image.load(actor["file"])
        actor["surf"] = pygame.transform.scale(
            actor["surf"], (size_actor, size_actor))
        actor["rect"] = actor["surf"].get_rect()
        left_position = (
            size_actor /
            1.5,
            ((i) *
             screen_rect.height /
             6) +
            screen_rect.height /
            100 +
            size_actor /
            2)
        right_position = (
            screen_rect.right - + size_actor / 1.5,
            ((i) * screen_rect.height / 6) + screen_rect.height
            / 100 + size_actor / 2)
        actor["rect"].center = left_position

        left_places.append([left_position, actor])
        right_places.append([right_position, None])

    actors.append(boat)

    action = None
    boatPlace = "left"
    step = 5
    to_dismount = None
    boat_passengers = [boat, None, None]

    fpsClock = pygame.time.Clock()

    while True:
        # print(boatPlace)
        window.blit(landscape, screen_rect.topleft)
        for actor in actors:
            window.blit(actor["surf"], actor["rect"])

        if action is None:
            event = eventListener()
            if event is not None:

                if event["id"] == boat_place1["id"]:
                    action = "dismount_boat"
                    to_dismount = event

                elif event["id"] == boat_place2["id"]:
                    action = "dismount_boat"
                    to_dismount = event

                elif event["id"] == "boat":
                    if boat_passengers[1] is not None \
                       or boat_passengers[2] is not None:
                        action = "ferry"

                else:
                    if boat_place1["id"] == "void":
                        # print(foundPosition(event))
                        # print(boatPlace)
                        if foundPosition(event) == boatPlace:
                            action = "mount_boat_1"
                            boat_place1 = event
                            boat_passengers[1] = event
                            updateSpacesStatus(event)
                            # print(boat)
                    elif boat_place2["id"] == "void":
                        if foundPosition(event) == boatPlace:
                            action = "mount_boat_2"
                            boat_place2 = event
                            boat_passengers[2] = event
                            updateSpacesStatus(event)
                            # print(boat)
        if action is not None:
            None

        if action == "check_solution":
            print("\n\n")
            game_state = gameState()
            print(game_state)
            print(gamegraph[game_state])

            if gamegraph[game_state] == "fail":
                return "¡¡¡YOU LOOSSEEE!!!"
            if gamegraph[game_state] == "success":
                return "¡¡¡YOU WINN!!!"

            action = None

        if action == "ferry":
            destination = boatLeftSide if boatPlace == "right" \
                          else boatRightSide
            done = ferry(boat_passengers, step, destination)
            if done:
                boatPlace = "left" if boatPlace == "right" else "right"
                action = "check_solution"

        if action == "mount_boat_1":
            done = mountBoat(boat_place1, boat, 1)
            if done:
                action = "check_solution"

        if action == "mount_boat_2":
            done = mountBoat(boat_place2, boat, 2)
            if done:
                action = "check_solution"

        if action == "dismount_boat":
            done = dismount(to_dismount)
            if done:
                action = "check_solution"

        pygame.display.flip()
        fpsClock.tick(120)


if __name__ == "__main__":
    game()
