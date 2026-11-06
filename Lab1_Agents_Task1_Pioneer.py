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
while robot: # main Control loop
    energy = World.getSensorReading("energySensor")
    ultrasonic_left = World.getSensorReading("ultraSonicSensorLeft")
    ultrasonic_right = World.getSensorReading("ultraSonicSensorRight")
    
    print("Distance: ", energy.distance)
    print("Direction: ", energy.direction)

    print("Left:", ultrasonic_left)
    print("Right:", ultrasonic_right)


    if(energy.direction < -0.2):
        motorSpeed = dict(speedLeft=0.5, speedRight=2)

    elif(energy.direction > 0.2):
        motorSpeed = dict(speedLeft=2, speedRight=0.5)

    else:
        motorSpeed = dict(speedLeft=2, speedRight=2)

    if(ultrasonic_left < 0.2 and ultrasonic_right < 0.2):
            motorSpeed = dict(speedLeft=-2, speedRight=-2)

    elif(ultrasonic_left < 0.5):
        motorSpeed = dict(speedLeft=2, speedRight=-2)

    elif(ultrasonic_right < 0.5):
        motorSpeed = dict(speedLeft=-2, speedRight=2)
    
    World.execute(motorSpeed, 100, -1) 
    World.collectNearestBlock()



