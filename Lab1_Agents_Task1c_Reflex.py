# Task 1c: REFLEX AGENT
# Uses the current sensor readings (energy sensor + 2 ultrasonic sensors), no memory.
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

    energy = World.getSensorReading("energySensor")
    ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
    ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")

    if energy.direction < -0.3:
        motorSpeed = dict(speedLeft=-1, speedRight=1)

    elif energy.direction > 0.3:
        motorSpeed = dict(speedLeft=1 , speedRight=-1)

    else:
        motorSpeed = dict(speedLeft=2, speedRight=2)

    if ultrasonic_left < 0.2 and ultrasonic_right < 0.2:
        motorSpeed = dict(speedLeft=-2, speedRight=-2)

    elif ultrasonic_left < 0.5:
        motorSpeed = dict(speedLeft=2, speedRight=-2)

    elif ultrasonic_right < 0.5:
        motorSpeed = dict(speedLeft=-2, speedRight=2)

    World.execute(motorSpeed, 100, -1)

    if World.collectNearestBlock() == "Energy collected :)":
        collectionTimes.append(World.getSimulationTime())
        print(f"Collected {len(collectionTimes)} blocks")


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
