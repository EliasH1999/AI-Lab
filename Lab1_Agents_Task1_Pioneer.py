# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
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
actions = [(dict(speedLeft=2, speedRight=2), 2000), 
               (dict(speedLeft=1, speedRight=-2), 500),
               (dict(speedLeft=2, speedRight=-1), 2000),
               (dict(speedLeft=-2, speedRight=-2), 500)]
while robot: # main Control loop
        for action, duration in actions: 
            World.execute(action, duration, -1)
            World.collectNearestBlock()

# 1c

