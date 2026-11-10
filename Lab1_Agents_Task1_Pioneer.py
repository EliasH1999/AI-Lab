# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
from turtle import right
from turtle import left

import Lab1_Agents_Task1_World_ZMQ as World
import random
import math
# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))


# 1a
# while robot: # main Control loop
#     motorSpeed = dict(speedLeft=random.choice([-2, -1, 0, 1, 2]), 
#                       speedRight=random.choice([-2, -1, 0, 1, 2]))



#     for i in range(2):
#         World.execute(motorSpeed, 500, -1)
#         World.collectNearestBlock()
#     sensor = World.getSensorReading("energySensor")
#     result = World.collectNearestBlock()
#     print(f"Distance: {sensor.distance:.2f} m | {result}")

# 1b
# actions = [(dict(speedLeft=2, speedRight=2), 6000), 
#                (dict(speedLeft=1, speedRight=2), 4000),
#                (dict(speedLeft=1, speedRight=2), 2000),
#                (dict(speedLeft=-2, speedRight=-2), 2000),]
# while robot: # main Control loop
#         for action, duration in actions: 
#             World.execute(action, duration, -1)
#             World.collectNearestBlock()

# 1c
# while robot: # main Control loop
#     energy = World.getSensorReading("energySensor")
#     ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
#     ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")
    
#     print("Distance: ", energy.distance)
#     print("Direction: ", energy.direction)

#     print("Left:", ultrasonic_left)
#     print("Right:", ultrasonic_right)


#     if(energy.direction < -0.2):
#         motorSpeed = dict(speedLeft=0.5, speedRight=2)

#     elif(energy.direction > 0.2):
#         motorSpeed = dict(speedLeft=2, speedRight=0.5)

#     else:
#         motorSpeed = dict(speedLeft=2, speedRight=2)

#     if(ultrasonic_left < 0.2 and ultrasonic_right < 0.2):
#             motorSpeed = dict(speedLeft=-2, speedRight=-2)

#     elif(ultrasonic_left < 0.5):
#         motorSpeed = dict(speedLeft=2, speedRight=-2)

#     elif(ultrasonic_right < 0.5):
#         motorSpeed = dict(speedLeft=-2, speedRight=2)
    
#     World.execute(motorSpeed, 100, -1) 
#     World.collectNearestBlock()

# 1d

# import random
# import math
# from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# previousDistance = 0
# stuckCounter = 0

# escaping = False
# escapeSteps = 0

# avoidDirection = None
# avoidTurnSteps = 4
# avoidForwardSteps = 10

# totalBlocks = 12
# targetBlocks = 6
# collectedBlocks = 0

# EXPLORE_TIMEOUT = 90000
# EXPLORE_DURATION = 60000

# lastBlockTime = World.getSimulationTime()

# exploring = False
# exploreStart = 0
# exploreDirection = None
# exploreTurnSteps = 0
# exploreForwardSteps = 0

# # Debugging
# debugIntervalMs = 500
# debugLastPrint = -debugIntervalMs
# debugLastKey = None

# debugClient = RemoteAPIClient()
# debugSim = debugClient.require("sim")
# debugRobotHandle = robot["pioneerRobotHandle"]


# while robot:  # Main control loop

#     debugNow = World.getSimulationTime()

#     energy = World.getSensorReading("energySensor")
#     ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
#     ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")

#     debugStuckBefore = stuckCounter
#     debugDistanceChange = None


# # Exploration logic
#     if exploring and debugNow - exploreStart >= EXPLORE_DURATION:

#         exploring = False
#         lastBlockTime = debugNow

#         previousDistance = 0
#         stuckCounter = 0

#         print(f"EXPLORATION FINISHED at {debugNow / 1000:.1f}s")

#     elif not exploring and debugNow - lastBlockTime >= EXPLORE_TIMEOUT:

#         exploring = True
#         exploreStart = debugNow

#         escaping = False
#         escapeSteps = 0
#         avoidDirection = None
#         avoidTurnSteps = 0
#         avoidForwardSteps = 0

#         previousDistance = 0
#         stuckCounter = 0

#         exploreTurnSteps = 0
#         exploreForwardSteps = 0

#         print(f"EXPLORATION STARTED at {debugNow / 1000:.1f}s")


# #Stuck detection logic
#     if not escaping and not exploring:

#         if previousDistance != 0:

#             debugDistanceChange = energy.distance - previousDistance

#             if abs(previousDistance - energy.distance) < 0.03:
#                 stuckCounter += 1
#             else:
#                 stuckCounter = 0

#         previousDistance = energy.distance

#         if stuckCounter > 25:

#             escaping = True
#             escapeSteps = 10
#             stuckCounter = 0

#             avoidDirection = None
#             avoidTurnSteps = 0
#             avoidForwardSteps = 0


# #Obstacle avoidance logic
#     if not escaping and avoidDirection is None:

#         if ultrasonic_left < 0.5 or ultrasonic_right < 0.5:

#             if ultrasonic_left < ultrasonic_right:
#                 avoidDirection = "right"
#             else:
#                 avoidDirection = "left"

#             avoidTurnSteps = 4
#             avoidForwardSteps = 10

#     debugAvoidBefore = avoidDirection

#     # ==========================================
#     # ORIGINAL ESCAPE
#     # ==========================================

#     if escaping:

#         debugMode = "ESCAPING"
#         debugReason = "ESCAPE_ACTIVE"

#         motorSpeed = dict(speedLeft=-2, speedRight=-1)
#         escapeSteps -= 1

#         if escapeSteps <= 0:
#             escaping = False
#             previousDistance = 0


# # Obstacle avoidance logic
#     elif avoidDirection is not None:

#         debugMode = "AVOIDING"

#         if ultrasonic_left < 0.2 and ultrasonic_right < 0.2:

#             debugReason = "BOTH_CLOSE"
#             motorSpeed = dict(speedLeft=-2, speedRight=-2)

#         elif ultrasonic_left < 0.2 or ultrasonic_right < 0.2:

#             debugReason = "ONE_CLOSE"

#             if avoidDirection == "left":
#                 motorSpeed = dict(speedLeft=-1, speedRight=1)
#             else:
#                 motorSpeed = dict(speedLeft=1, speedRight=-1)

#         elif avoidTurnSteps > 0:

#             debugReason = "TURNING"

#             if avoidDirection == "left":
#                 motorSpeed = dict(speedLeft=-1, speedRight=1)
#             else:
#                 motorSpeed = dict(speedLeft=1, speedRight=-1)

#             avoidTurnSteps -= 1

#         elif avoidForwardSteps > 0:

#             debugReason = "MOVING_FORWARD"

#             motorSpeed = dict(speedLeft=1, speedRight=1)
#             avoidForwardSteps -= 1

#         else:

#             debugReason = "AVOID_FINISHED"
#             avoidDirection = None
#             motorSpeed = dict(speedLeft=1, speedRight=1)



# # Exploration logic
#     elif exploring:

#         debugMode = "EXPLORING"

#         if exploreTurnSteps > 0:

#             debugReason = "RANDOM_TURN"
#             exploreTurnSteps -= 1

#             if exploreDirection == "left":
#                 motorSpeed = dict(speedLeft=-1, speedRight=1)
#             else:
#                 motorSpeed = dict(speedLeft=1, speedRight=-1)

#         elif exploreForwardSteps > 0:

#             debugReason = "RANDOM_FORWARD"
#             exploreForwardSteps -= 1

#             motorSpeed = dict(speedLeft=1.5, speedRight=1.5)

#         else:

#             # Choose a new random direction
#             exploreDirection = random.choice(["left", "right"])
#             exploreTurnSteps = random.randint(3, 6) - 1
#             exploreForwardSteps = random.randint(15, 25)

#             debugReason = "RANDOM_TURN"

#             if exploreDirection == "left":
#                 motorSpeed = dict(speedLeft=-1, speedRight=1)
#             else:
#                 motorSpeed = dict(speedLeft=1, speedRight=-1)


# #Original block collection logic
#     else:

#         debugMode = "NORMAL"

#         if energy.direction < -0.2:

#             debugReason = "BLOCK_LEFT"
#             motorSpeed = dict(speedLeft=0.5, speedRight=2)

#         elif energy.direction > 0.2:

#             debugReason = "BLOCK_RIGHT"
#             motorSpeed = dict(speedLeft=2, speedRight=0.5)

#         else:

#             debugReason = "BLOCK_AHEAD"
#             motorSpeed = dict(speedLeft=2, speedRight=2)

#     # ==========================================
#     # DEBUG OUTPUT
#     # ==========================================

#     debugKey = (
#         debugMode,
#         debugReason,
#         debugAvoidBefore,
#         motorSpeed["speedLeft"],
#         motorSpeed["speedRight"]
#     )

#     if (
#         debugKey != debugLastKey
#         or debugNow - debugLastPrint >= debugIntervalMs
#         or (debugMode == "ESCAPING" and escapeSteps == 0)
#     ):

#         debugDelta = (
#             "n/a" if debugDistanceChange is None
#             else f"{debugDistanceChange:+.3f}m"
#         )

#         debugYaw = debugSim.getObjectOrientation(
#             debugRobotHandle, -1
#         )[2]

#         print(
#             f"t={debugNow / 1000:.2f}s "
#             f"{debugMode}/{debugReason} "
#             f"worldYaw_deg={math.degrees(debugYaw):+.2f} "
#             f"| block={energy.distance:.3f}m "
#             f"angle={energy.direction:+.3f}rad"
#             f"({math.degrees(energy.direction):+.1f}deg) "
#             f"| sonarL={ultrasonic_left:.3f}m "
#             f"sonarR={ultrasonic_right:.3f}m "
#             f"| wheels=("
#             f"{motorSpeed['speedLeft']:.1f},"
#             f"{motorSpeed['speedRight']:.1f}) "
#             f"| avoid={debugAvoidBefore}->{avoidDirection} "
#             f"stuck={debugStuckBefore}->{stuckCounter} "
#             f"delta={debugDelta} "
#             f"escapeLeft={escapeSteps} "
#             f"avoidLeft={avoidForwardSteps}"
#         )

#         debugLastPrint = debugNow
#         debugLastKey = debugKey


#     World.execute(motorSpeed, 100, -1)
#     debugCollection = World.collectNearestBlock()

#     if debugCollection == "Energy collected :)":

#         collectedBlocks += 1
#         lastBlockTime = World.getSimulationTime()

#         exploring = False
#         exploreTurnSteps = 0
#         exploreForwardSteps = 0

#         print(f"Collected {collectedBlocks}/{targetBlocks} blocks")
#         print(debugCollection)

#     # ==========================================
#     # STOP AFTER SIX BLOCKS
#     # ==========================================

#     if collectedBlocks >= targetBlocks:

#         print("\n========== FINAL RESULTS ==========")
#         print(f"Blocks collected: {collectedBlocks}/{totalBlocks}")
#         print(f"Simulation time: {World.getSimulationTime() / 1000:.1f}s")
#         print("===================================")

#         motorSpeed = dict(speedLeft=0, speedRight=0)
#         World.execute(motorSpeed, 100, -1)
#         break






import random

# Memory
previousDistance = 0
stuckCounter = 0

escaping = False
escapeSteps = 0

avoidDirection = None
avoidTurnSteps = 4
avoidForwardSteps = 10

# Block collection
totalBlocks = 12
targetBlocks = 6
collectedBlocks = 0

# Exploration
EXPLORE_TIMEOUT = 90000
EXPLORE_DURATION = 60000

lastBlockTime = World.getSimulationTime()

exploring = False
exploreStart = 0
exploreDirection = None
exploreTurnSteps = 0
exploreForwardSteps = 0

# Debugging
lastDebugTime = -500
lastMode = None

while robot:
    now = World.getSimulationTime()

    energy = World.getSensorReading("energySensor")
    ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
    ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")

    # Exploration timing
    if exploring and now - exploreStart >= EXPLORE_DURATION:
        exploring = False
        lastBlockTime = now

        previousDistance = 0
        stuckCounter = 0

    elif not exploring and now - lastBlockTime >= EXPLORE_TIMEOUT:
        exploring = True
        exploreStart = now

        escaping = False
        escapeSteps = 0
        avoidDirection = None
        avoidTurnSteps = 0
        avoidForwardSteps = 0

        previousDistance = 0
        stuckCounter = 0

        exploreTurnSteps = 0
        exploreForwardSteps = 0

    # Stuck detection
    if not escaping and not exploring:
        if previousDistance != 0:
            if abs(previousDistance - energy.distance) < 0.03:
                stuckCounter += 1
            else:
                stuckCounter = 0

        previousDistance = energy.distance

        if stuckCounter > 25:
            escaping = True
            escapeSteps = 10
            stuckCounter = 0

            avoidDirection = None
            avoidTurnSteps = 0
            avoidForwardSteps = 0

    # Activate obstacle avoidance
    if not escaping and avoidDirection is None:
        if ultrasonic_left < 0.5 or ultrasonic_right < 0.5:
            if ultrasonic_left < ultrasonic_right:
                avoidDirection = "right"
            else:
                avoidDirection = "left"

            avoidTurnSteps = 4
            avoidForwardSteps = 10

    # MODE 1: ESCAPING
    if escaping:
        mode = "ESCAPING"

        motorSpeed = dict(speedLeft=-2, speedRight=-1)
        escapeSteps -= 1

        if escapeSteps <= 0:
            escaping = False
            previousDistance = 0

    # MODE 2: AVOIDING
    elif avoidDirection is not None:
        mode = "AVOIDING"

        if ultrasonic_left < 0.2 and ultrasonic_right < 0.2:
            motorSpeed = dict(speedLeft=-2, speedRight=-2)

        elif ultrasonic_left < 0.2 or ultrasonic_right < 0.2:
            if avoidDirection == "left":
                motorSpeed = dict(speedLeft=-1, speedRight=1)
            else:
                motorSpeed = dict(speedLeft=1, speedRight=-1)

        elif avoidTurnSteps > 0:
            if avoidDirection == "left":
                motorSpeed = dict(speedLeft=-1, speedRight=1)
            else:
                motorSpeed = dict(speedLeft=1, speedRight=-1)

            avoidTurnSteps -= 1

        elif avoidForwardSteps > 0:
            motorSpeed = dict(speedLeft=1, speedRight=1)
            avoidForwardSteps -= 1

        else:
            avoidDirection = None
            motorSpeed = dict(speedLeft=1, speedRight=1)

    # MODE 3: EXPLORING
    elif exploring:
        mode = "EXPLORING"

        if exploreTurnSteps == 0 and exploreForwardSteps == 0:
            exploreDirection = random.choice(["left", "right"])
            exploreTurnSteps = random.randint(3, 6)
            exploreForwardSteps = random.randint(15, 25)

        if exploreTurnSteps > 0:
            exploreTurnSteps -= 1

            if exploreDirection == "left":
                motorSpeed = dict(speedLeft=-1, speedRight=1)
            else:
                motorSpeed = dict(speedLeft=1, speedRight=-1)

        elif exploreForwardSteps > 0:
            exploreForwardSteps -= 1
            motorSpeed = dict(speedLeft=1.5, speedRight=1.5)

    # MODE 4: NORMAL
    else:
        mode = "NORMAL"

        if energy.direction < -0.2:
            motorSpeed = dict(speedLeft=0.5, speedRight=2)

        elif energy.direction > 0.2:
            motorSpeed = dict(speedLeft=2, speedRight=0.5)

        else:
            motorSpeed = dict(speedLeft=2, speedRight=2)

    # Compact debugging: every 500ms or on mode change
    if mode != lastMode or now - lastDebugTime >= 500:
        print(
            f"{now / 1000:.1f}s | {mode} | "
            f"Block: {energy.distance:.2f}m "
            f"({energy.direction:.2f}rad) | "
            f"L: {ultrasonic_left:.2f} "
            f"R: {ultrasonic_right:.2f} | "
            f"Motors: {motorSpeed['speedLeft']}, "
            f"{motorSpeed['speedRight']}"
        )

        lastDebugTime = now
        lastMode = mode

    # Execute movement and collect blocks
    World.execute(motorSpeed, 100, -1)
    result = World.collectNearestBlock()

    if result == "Energy collected :)":
        collectedBlocks += 1
        lastBlockTime = World.getSimulationTime()

        exploring = False
        exploreTurnSteps = 0
        exploreForwardSteps = 0

        print(f"Collected {collectedBlocks}/{targetBlocks} blocks")

    # Stop after six blocks
    if collectedBlocks >= targetBlocks:
        print("\n========== FINAL RESULTS ==========")
        print(f"Blocks collected: {collectedBlocks}/{totalBlocks}")
        print(f"Simulation time: {World.getSimulationTime() / 1000:.1f}s")
        print("===================================")

        motorSpeed = dict(speedLeft=0, speedRight=0)
        World.execute(motorSpeed, 100, -1)
        break
