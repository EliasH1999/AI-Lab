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


import Lab1_Agents_Task1_World_ZMQ as World
import random
import math
# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))



import random
import Lab1_Agents_Task1_World_ZMQ as World


# Performance measurements
MAX_TIME = 1200000  # 20 minutes in milliseconds
startTime = World.getSimulationTime()
collectionTimes = []



# 1a - RANDOM AGENT

# while robot:
#     if World.getSimulationTime() - startTime >= MAX_TIME:
#         break

#     motorSpeed = dict(
#         speedLeft=random.choice([-2, -1, 0, 1, 2]),
#         speedRight=random.choice([-2, -1, 0, 1, 2])
#     )

#     World.execute(motorSpeed, 100, -1)

#     if World.collectNearestBlock() == "Energy collected :)":
#         collectionTimes.append(World.getSimulationTime())


# # FINAL RESULTS
# World.execute(dict(speedLeft=0, speedRight=0), 100, -1)

# print("\n========== FINAL RESULTS ==========")
# print(f"Blocks collected: {len(collectionTimes)}")
# print(f"Simulation time: {(World.getSimulationTime() - startTime) / 1000:.1f}s")

# if collectionTimes:
#     firstBlockTime = (collectionTimes[0] - startTime) / 1000
#     print(f"Time to first block: {firstBlockTime:.2f}s")
# else:
#     print("Time to first block: N/A")

# if len(collectionTimes) >= 2:
#     averageTime = (collectionTimes[-1] - collectionTimes[0]) / (len(collectionTimes) - 1) / 1000
#     print(f"Average time between collections: {averageTime:.2f}s")
# else:
#     print("Average time between collections: N/A")

# print("===================================")



# 1b - FIXED AGENT

# actions = [
#     (dict(speedLeft=2, speedRight=2), 6000),
#     (dict(speedLeft=1, speedRight=2), 4000),
#     (dict(speedLeft=1, speedRight=2), 2000),
#     (dict(speedLeft=-2, speedRight=-2), 2000),
# ]

# while robot:
#     if World.getSimulationTime() - startTime >= MAX_TIME:
#         break

#     for action, duration in actions:
#         if World.getSimulationTime() - startTime >= MAX_TIME:
#             break

#         World.execute(action, duration, -1)

#         if World.collectNearestBlock() == "Energy collected :)":
#             collectionTimes.append(World.getSimulationTime())
#             print(f"Collected {len(collectionTimes)} blocks")


# # FINAL RESULTS
# World.execute(dict(speedLeft=0, speedRight=0), 100, -1)

# print("\n========== FINAL RESULTS ==========")
# print(f"Blocks collected: {len(collectionTimes)}")
# print(f"Simulation time: {(World.getSimulationTime() - startTime) / 1000:.1f}s")

# if collectionTimes:
#     firstBlockTime = (collectionTimes[0] - startTime) / 1000
#     print(f"Time to first block: {firstBlockTime:.2f}s")
# else:
#     print("Time to first block: N/A")

# if len(collectionTimes) >= 2:
#     averageTime = (collectionTimes[-1] - collectionTimes[0]) / (len(collectionTimes) - 1) / 1000
#     print(f"Average time between collections: {averageTime:.2f}s")
# else:
#     print("Average time between collections: N/A")

# print("===================================")



# 1c - REFLEX AGENT

# while robot:
#     if World.getSimulationTime() - startTime >= MAX_TIME:
#         break

#     energy = World.getSensorReading("energySensor")
#     ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
#     ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")

#     if energy.direction < -0.3:
#         motorSpeed = dict(speedLeft=-1, speedRight=1)

#     elif energy.direction > 0.3:
#         motorSpeed = dict(speedLeft=1 , speedRight=-1)

#     else:
#         motorSpeed = dict(speedLeft=2, speedRight=2)

#     if ultrasonic_left < 0.2 and ultrasonic_right < 0.2:
#         motorSpeed = dict(speedLeft=-2, speedRight=-2)

#     elif ultrasonic_left < 0.5:
#         motorSpeed = dict(speedLeft=2, speedRight=-2)

#     elif ultrasonic_right < 0.5:
#         motorSpeed = dict(speedLeft=-2, speedRight=2)

#     World.execute(motorSpeed, 100, -1)

#     if World.collectNearestBlock() == "Energy collected :)":
#         collectionTimes.append(World.getSimulationTime())
#         print(f"Collected {len(collectionTimes)} blocks")


# # FINAL RESULTS
# World.execute(dict(speedLeft=0, speedRight=0), 100, -1)

# print("\n========== FINAL RESULTS ==========")
# print(f"Blocks collected: {len(collectionTimes)}")
# print(f"Simulation time: {(World.getSimulationTime() - startTime) / 1000:.1f}s")

# if collectionTimes:
#     firstBlockTime = (collectionTimes[0] - startTime) / 1000
#     print(f"Time to first block: {firstBlockTime:.2f}s")
# else:
#     print("Time to first block: N/A")

# if len(collectionTimes) >= 2:
#     averageTime = (collectionTimes[-1] - collectionTimes[0]) / (len(collectionTimes) - 1) / 1000
#     print(f"Average time between collections: {averageTime:.2f}s")
# else:
#     print("Average time between collections: N/A")

# print("===================================")







# Performance measurements
MAX_TIME = 1200000  # 20 minutes in milliseconds
startTime = World.getSimulationTime()
collectionTimes = []

# 1d - MEMORY AGENT

# Settings
SAFE_LEFT = 0.6           # start avoiding when the left sonar reads less than this (m)
SAFE_RIGHT = 0.9      # the right sonar looks almost straight ahead, so it needs a bigger margin
SAFE_NEAR_BLOCK = 0.3    # used for both sonars when the block is right in front of us
CLEAR_DISTANCE = 0.5     # keep turning until both sonars read more than this (m)
EXTRA_TURN_TIME = 1250  # keep turning this long after the wall is out of view (ms)
PASS_TIME = 2000         # then drive straight this long to get past the wall (ms)

STUCK_TIMEOUT = 10000    # no progress towards the block for this long -> explore (ms)
EXPLORE_START = 15000    # first exploration lasts this long (ms)
EXPLORE_MAX = 60000      # exploration never lasts longer than this (ms)

# Memory
bestDistance = float("inf")     # closest we have been to the current block
lastProgressTime = startTime    # when we last got closer to it

exploring = False
exploreUntil = 0
exploreTime = EXPLORE_START     # doubles every time we get stuck on the same block

avoidDirection = None           # which way we started turning at the current wall
turnUntil = 0
passUntil = 0

# Debugging
lastDebugTime = 0
lastMode = None

while robot:
    now = World.getSimulationTime()

    if now - startTime >= MAX_TIME:
        break

    energy = World.getSensorReading("energySensor")
    ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
    ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")

    # Collected blocks are moved far away, so this means there are none left
    if energy.distance > 100:
        print("All blocks collected")
        break

    # Progress memory: are we still getting closer to the block?
    if not exploring:
        if energy.distance < bestDistance - 0.1:
            bestDistance = energy.distance
            lastProgressTime = now

        elif now - lastProgressTime >= STUCK_TIMEOUT:
            exploring = True
            exploreUntil = now + exploreTime
            exploreTime = min(exploreTime * 2, EXPLORE_MAX)

    elif now >= exploreUntil:
        exploring = False
        bestDistance = energy.distance
        lastProgressTime = now

    # Allow going closer to a wall when the block is right in front of us
    if not exploring and energy.distance < 1.0 and abs(energy.direction) < 0.3:
        safeLeft = SAFE_NEAR_BLOCK
        safeRight = SAFE_NEAR_BLOCK
    else:
        safeLeft = SAFE_LEFT
        safeRight = SAFE_RIGHT

    # Activate obstacle avoidance and remember which way we turn
    if avoidDirection is None:
        if ultrasonic_left < safeLeft or ultrasonic_right < safeRight:
            if ultrasonic_left < ultrasonic_right:
                avoidDirection = "right"
            else:
                avoidDirection = "left"
            turnUntil = now + EXTRA_TURN_TIME
            passUntil = turnUntil + PASS_TIME


    # While the wall is still in view, keep pushing the turn/pass timers forward
    if avoidDirection is not None:
        if ultrasonic_left < CLEAR_DISTANCE or ultrasonic_right < CLEAR_DISTANCE:
            turnUntil = now + EXTRA_TURN_TIME
            passUntil = turnUntil + PASS_TIME

        elif now >= passUntil:
            avoidDirection = None

    # MODE 1: AVOIDING - turn on the spot until the wall is well out of the way
    if avoidDirection is not None and now < turnUntil:
        mode = "AVOIDING"

        if avoidDirection == "left":
            motorSpeed = dict(speedLeft=-1, speedRight=1)
        else:
            motorSpeed = dict(speedLeft=1, speedRight=-1)

    # MODE 2: PASSING - drive straight for a while to get past the wall
    elif avoidDirection is not None:
        mode = "PASSING"

        motorSpeed = dict(speedLeft=2, speedRight=2)

    # MODE 3: EXPLORING - drive straight, the walls decide where we end up
    elif exploring:
        mode = "EXPLORING"

        motorSpeed = dict(speedLeft=2, speedRight=2)

    # MODE 4: NORMAL - turn on the spot towards the block, then drive straight
    else:
        mode = "NORMAL"

        if energy.direction < -0.3:
            motorSpeed = dict(speedLeft=-1, speedRight=1)

        elif energy.direction > 0.3:
            motorSpeed = dict(speedLeft=1, speedRight=-1)

        else:
            motorSpeed = dict(speedLeft=2, speedRight=2)

    # Compact debugging
    if mode != lastMode or now - lastDebugTime >= 2000:
        print(
            f"{now / 1000:.1f}s | {mode} | "
            f"Block: {energy.distance:.2f}m ({energy.direction:.2f}rad) | "
            f"L: {ultrasonic_left:.2f} R: {ultrasonic_right:.2f} | "
            f"Best: {bestDistance:.2f}m"
        )

        lastDebugTime = now
        lastMode = mode

    # Execute movement
    World.execute(motorSpeed, 100, -1)

    # Collect energy blocks
    if World.collectNearestBlock() == "Energy collected :)":
        collectionTimes.append(World.getSimulationTime())
        print(f"Collected {len(collectionTimes)} blocks")

        # New target: forget everything about the old one
        bestDistance = float("inf")
        lastProgressTime = World.getSimulationTime()
        exploring = False
        exploreTime = EXPLORE_START


# FINAL RESULTS (runs after the control loop finishes)
World.execute(dict(speedLeft=0, speedRight=0), 100, -1)

print("\n========== FINAL RESULTS ==========")
print(f"Blocks collected: {len(collectionTimes)}")
print(f"Simulation time: {(World.getSimulationTime() - startTime) / 1000:.1f}s")

if collectionTimes:
    firstBlockTime = (collectionTimes[0] - startTime) / 1000
    print(f"Time to first block: {firstBlockTime:.2f}s")
else:
    print("Time to first block: N/A")

if len(collectionTimes) >= 2:
    averageTime = (collectionTimes[-1] - collectionTimes[0]) / (len(collectionTimes) - 1) / 1000
    print(f"Average time between collections: {averageTime:.2f}s")
else:
    print("Average time between collections: N/A")

print("===================================")