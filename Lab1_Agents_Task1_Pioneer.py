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

previousDistance = 0
stuckCounter = 0

escaping = False
escapeSteps = 0

avoidDirection = None
avoidForwardSteps = 10


while robot: # main Control loop
    energy = World.getSensorReading("energySensor")
    ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
    ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")

    # If it's not escaping, check if it's stuck. If it is, start escaping.
    if not escaping:
        if previousDistance is not 0:
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
            avoidForwardSteps = 0
    # If it's not escaping and not avoiding, check if it needs to avoid an obstacle.
    if not escaping and avoidDirection is None:
        if ultrasonic_left < 0.5 or ultrasonic_right < 0.5:
            if ultrasonic_left < ultrasonic_right:
                avoidDirection = "right"
            else:
                avoidDirection = "left"
            avoidForwardSteps = 10
            
    # Mode 1: Escaping
    if escaping: 
        motorSpeed = dict(speedLeft=-2, speedRight=-1)
        escapeSteps -= 1

        if escapeSteps <= 0:
            escaping = False
            previousDistance = 0
    # Mode 2: Avoiding
    elif avoidDirection is not None:
        # Very close on both sides: back away.
        if ultrasonic_left < 0.2 and ultrasonic_right < 0.2:
            motorSpeed = dict(speedLeft=-1, speedRight=-1)
            avoidForwardSteps = 10

        # Keep the chosen turn direction until there is clearance.
        elif ultrasonic_left < 0.6 or ultrasonic_right < 0.6:
            if avoidDirection == "left":
                motorSpeed = dict(speedLeft=-1, speedRight=1)
            else:
                motorSpeed = dict(speedLeft=1, speedRight=-1)

            avoidForwardSteps = 10

        # Move forward while checking clearance on every loop.
        elif avoidForwardSteps > 0:
            motorSpeed = dict(speedLeft=1, speedRight=1)
            avoidForwardSteps -= 1

        else:
            avoidDirection = None
            motorSpeed = dict(speedLeft=0, speedRight=0)
    # Mode 3: Normal
    else:
        if(energy.direction < -0.2):
            motorSpeed = dict(speedLeft=0.5, speedRight=2)

        elif(energy.direction > 0.2):
            motorSpeed = dict(speedLeft=2, speedRight=0.5)

        else:
             motorSpeed = dict(speedLeft=2, speedRight=2)

    if escaping:
        print("MODE: ESCAPING")

    elif avoidDirection is not None:
        print("MODE: AVOIDING", avoidDirection)

    else:
        print("MODE: NORMAL")
    World.execute(motorSpeed, 100, -1)
    World.collectNearestBlock()
    # if not escaping:
    #     if previousDistance is not 0:
    #         if abs(previousDistance - energy.distance) < 0.03:
    #             stuckCounter += 1
    #         else: 
    #             stuckCounter = 0

    #     previousDistance = energy.distance

    # if stuckCounter > 25:
    #     escaping = True
    #     escapeSteps = 10
    #     stuckCounter = 0

    # if escaping:
    #     motorSpeed = dict(speedLeft=-2, speedRight=-1)
    #     escapeSteps -= 1

    #     if escapeSteps <= 0:
    #         escaping = False
    #         previousDistance = 0
    # else:
    #     previousDistance = energy.distance
    #     print("Stuck counter: ", stuckCounter)

    #     ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
    #     ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")
        
    #     print("Distance: ", energy.distance)
    #     print("Direction: ", energy.direction)

    #     print("Left:", ultrasonic_left)
    #     print("Right:", ultrasonic_right)

    #     if(avoidDirection is None):
    #         if ultrasonic_left < 0.2 or ultrasonic_right < 0.2:
    #             if ultrasonic_left < ultrasonic_right:
    #                 avoidDirection = "right"
    #             else:
    #                 avoidDirection = "left"
                
    #             clearSteps = 0

    #     else:
    #         if(ultrasonic_left > 0.3 and ultrasonic_right > 0.3):
    #             clearSteps += 1
    #         else:
    #             clearSteps = 0
    #         if(clearSteps > 15):
    #             avoidDirection = None
    #             clearSteps = 0
    #     if(avoidDirection == "left"):
    #         motorSpeed = dict(speedLeft=0.2, speedRight=1.5)

    #     elif(avoidDirection == "right"):
    #         motorSpeed = dict(speedLeft=1.5, speedRight=0.2)

    #     elif(energy.direction < -0.2):
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
    # World.execute(motorSpeed, 100, -1) 
    # World.collectNearestBlock()


