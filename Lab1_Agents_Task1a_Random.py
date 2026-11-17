
# Task 1a: RANDOM AGENT
# Picks random wheel speeds, ignores all sensor input.
# How to run: open Lab1_Agents_Task1_World.ttt in CoppeliaSim, press Play,
# then run this file. Lab1_Agents_Task1_World_ZMQ.py must be in the same folder.

import random
import Lab1_Agents_Task1_World_ZMQ as World

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

# Performance measurements
MAX_TIME = 1200000  # 20 minutes in milliseconds
startTime = World.getSimulationTime()
collectionTimes = []


while robot:
    if World.getSimulationTime() - startTime >= MAX_TIME:
        break

    motorSpeed = dict(
        speedLeft=random.choice([-2, -1, 0, 1, 2]),
        speedRight=random.choice([-2, -1, 0, 1, 2])
    )

    World.execute(motorSpeed, 100, -1)

    if World.collectNearestBlock() == "Energy collected :)":
        collectionTimes.append(World.getSimulationTime())


# FINAL RESULTS
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
