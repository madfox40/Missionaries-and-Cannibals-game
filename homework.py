import random
import sys
import pygame




def ferry(passengers, step, position):
    """
    who Position [0] is the leader
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
                    actor["rect"] = actor["rect"].move((-dist_to_goal_x, 0))
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
                actor["rect"] = actor["rect"].move((0,-step))
        else:
            for actor in who:
                actor["rect"] = actor["rect"].move((0,step))

    if position == leader["rect"].center:
        for actor in who:
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
        done = True

    #for actor in who:
        #print(actor["rect"].center)
    #print(position)

    return done

boat_place1 = {"id": "void"}
boat_place2 = {"id": "void"}
def freePos(who):
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
    for position in right_places:
        if position[1] is not None:
            if position[1]["id"] == who["id"]:
                return "right"
    for position in left_places:
        if position[1] is not None:
            if position[1]["id"] == who["id"]:
                return "left"

def freeBoatPos(who):
    global boat_place1
    global boat_place2
    if boat_place1["id"] == who["id"]:
        boat_place1 = {"id":"void"}
        boat_passengers[1] = None
        print(f"Desmounted {who['id']}")


    if boat_place2["id"] == who["id"]:
        boat_place2 = {"id": "void"}
        boat_place2["id"] = "void"
        boat_passengers[2] = None
        print(f"Desmounted {who['id']}")



def mountBoat(who, boat, position):
    boat_long = boat["rect"].right - boat["rect"].left
    if position == 1:
        #print((boat["rect"].centerx/4 * 1, boat["rect"].centery+ height* 0,1 ))
        done = ferry([who], step, (boat["rect"].left + (boat_long/4 * 1),boat["rect"].centery - height * 0.1))
        if done:
            freePos(who)
            #printLibreSpaces()
        return done
    else:
        done = ferry([who], step, (boat["rect"].left + (boat_long/4 * 3),boat["rect"].centery - height* 0.1) )
        if done:
            freePos(who)
            #printLibreSpaces()
        return done

def dismount(who):
    #printLibreSpaces()
    if boatPlace == "right":
        for i, space in enumerate(right_places):

            #If space is not occuppied
            if space[1] is None:
                #We move "who" to the space
                # and if movement is finished
                if( ferry([who], step, (space[0]))):
                    #We occuppied the space
                    space[1] = who
                    #printLibreSpaces()
                    freeBoatPos(who)
                    #The movement is finished
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
                    #printLibreSpaces()
                    freeBoatPos(who)
                    #The movement is finished
                    return True
                # The space is being reached, so we don't
                # want to search for more spaces
                break

    #The movement is not finished
    return False

def printLibreSpaces():
    print("\n\n")
    for i, place in enumerate(left_places):
        if place[1] is None:
            print(f"Izquierda: {i}, {place[0]},0")
        else:
            print(f"Izquierda: {i}, {place[0]}, Ocupied")

    print("\n\n")
    for i, place in enumerate(right_places):
        if place[1] is None:
            print(f"Derecha: {i}, {place[0]}, 0")
        else:
            print(f"Derecha: {i}, {place[0]}, Ocupied")




def failure():
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = screen_rect.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)

def success():
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Success", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = screen_rect.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)

pygame.init()
width = 800
height = 480
window = pygame.display.set_mode((width, height))
screen_rect = window.get_rect()
landscape = pygame.image.load("images/landscape2.jpg").convert()
landscape = pygame.transform.scale(landscape, (width,height))


missionarie1 = {"file": "images/baby.png", "id": "missionarie1"}
missionarie2 = {"file": "images/baby.png", "id": "missionarie2"}
missionarie3 = {"file": "images/baby.png", "id": "missionarie3"}

cannibal1 = {"file": "images/cannibal.png", "id": "cannibal1"}
cannibal2 = {"file": "images/cannibal.png", "id": "cannibal2"}
cannibal3 = {"file": "images/cannibal.png", "id": "cannibal3"}

boatLeftSide = (screen_rect.width/7 * 2, screen_rect.centery)
boatRightSide = (screen_rect.width/7 * 5, screen_rect.centery)
boat = {"id": "boat"}
boat["surf"] = pygame.image.load("images/boat.png")
boat["surf"] = pygame.transform.scale(boat["surf"], (screen_rect.width/ 4, screen_rect.height / 4))
boat["rect"] = boat["surf"].get_rect()
boat["rect"].center = boatLeftSide

def updateSpacesStatus(last_movement_object):
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

def clikListener():
    """
    If an actor is clicked it returns it
    """
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, actor in enumerate(actors):
                if actor["rect"].collidepoint(mouse_pos):
                    return actor
    else:
        return

actors = [missionarie1, missionarie2, missionarie3, cannibal1, cannibal2, cannibal3]


right_places = []
left_places = []

for i in right_places:
    i[0] = i[0] + (screen_rect.height / 100)
for i in right_places:
    i[0] = i[0] + (screen_rect.height / 100)


for i, actor in enumerate(actors):
    size_actor = screen_rect.height/ 8
    actor["surf"] = pygame.image.load(actor["file"])
    actor["surf"] = pygame.transform.scale(actor["surf"], (size_actor, size_actor))
    actor["rect"] = actor["surf"].get_rect()
    left_position = (size_actor/1.5, ((i) * screen_rect.height / 6 ) + screen_rect.height / 100 + size_actor/2)
    right_position = (screen_rect.right - + size_actor/1.5 , ((i) * screen_rect.height / 6) + screen_rect.height / 100 + size_actor/2)
    actor["rect"].center = left_position

    left_places.append([left_position, actor])
    right_places.append([right_position,None])
    #actor["surf"].fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

#print(left_places)
actors.append(boat)


gamegraph = {
            "wgcf-": {"f": "wgc-f", "w": "gc-wf", "g": "wc-gf", "c": "wg-cf"},
            "wc-gf": {"f": "wcf-g", "g": "wgcf-"},
            "gc-wf": "failure",
                "gcf-w": {"f": "gc-wf", "g": "c-wgf", "c": "g-wcf"},
                    "c-wgf": {"f": "cf-wg", "w": "wcf-g", "g": "gcf-w"},
                        "cf-wg": "failure",
                    "g-wcf": {"f": "gf-wc", "w": "wgf-c", "c": "gcf-w"},
                        "gf-wc": {"f": "g-wcf", "g": "-wgcf"},
            "wg-cf": "failure",
                "wgf-c": {"f": "wg-cf", "g": "w-gcf", "w": "g-wcf"},
                    "w-gcf": {"f": "wf-gc", "g": "wgf-c", "c": "wcf-g"},
                        "wf-gc": "failure",
            "wcf-g": {"f": "wc-gf" , "c": "w-gcf", "w": "c-wgf"} ,
            "wgc-f": "failure",
            "-wgcf": "success"}

gamestate = "wgcf-"
controls = {pygame.K_f: "f", pygame.K_g: "g", pygame.K_c: "c", pygame.K_w: "w"}
#passengers = {"f": [farm], "g": [farm, goat], "c": [farm, cabb], "w": [farm, wolf]}
ferry_step = -5
action = None
boatPlace = "left"
step = 5

boat_passengers = [boat, None, None]


to_dismount = None

fpsClock = pygame.time.Clock()
#printLibreSpaces()
while True:
    #print(boatPlace)
    window.blit(landscape, screen_rect.topleft)
    for actor in actors:
        window.blit(actor["surf"], actor["rect"])


    if action is None:
        event = clikListener()
        if event is not None:


            if event["id"] == boat_place1["id"]:
                action = "dismount_boat"
                to_dismount = event


            elif event["id"] == boat_place2["id"]:
                action = "dismount_boat"
                to_dismount = event



            elif event["id"] == "boat":
                if boat_passengers[1] is not None or boat_passengers[2] is not None:
                    action = "ferry"


            elif event["id"] != boat_place1["id"] and event["id"] != boat_place2["id"]:
                if boat_place1["id"] == "void":
                    print(foundPosition(event))
                    print(boatPlace)
                    if foundPosition(event) == boatPlace:
                        action = "mount_boat_1"
                        boat_place1 = event
                        boat_passengers[1] = event
                        updateSpacesStatus(event)
                        print(boat)
                elif boat_place2["id"] == "void":
                    if foundPosition(event) == boatPlace:
                        action = "mount_boat_2"
                        boat_place2 = event
                        boat_passengers[2] = event
                        updateSpacesStatus(event)
                        print(boat)
    if action is not None:
        None
        #print(action)
    if action == "ferry":
        destination = boatLeftSide  if boatPlace == "right" else boatRightSide
        done = ferry(boat_passengers, step, destination)
        if done:
            boatPlace = "left" if boatPlace == "right" else "right"
            action = None


    if action == "mount_boat_1":
        done = mountBoat(boat_place1,boat,1)
        if done:
            action = None

    if action == "mount_boat_2":
        done = mountBoat(boat_place2,boat,2)
        if done:
            action = None

    if action == "dismount_boat":
        done = dismount(to_dismount)
        if done:
            action = None


    pygame.display.flip()
    fpsClock.tick(120)
