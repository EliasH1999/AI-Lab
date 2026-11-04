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
while robot: # main Control loop
    motorSpeed = dict(speedLeft=random.choice([-2, -1, 0, 1, 2]), 
                      speedRight=random.choice([-2, -1, 0, 1, 2]))



    for i in range(2):
        World.execute(motorSpeed, 500, -1)
        World.collectNearestBlock()
    sensor = World.getSensorReading("energySensor")
    result = World.collectNearestBlock()
    print(f"Distance: {sensor.distance:.2f} m | {result}")

# 1b

    # #######################################################
    # # Perception Phase: Get information about environment #
    # #######################################################
    # simulationTime = World.getSimulationTime()
    # if simulationTime%1000==0:
    #     # print some useful info, but not too often
    #     print ('Time:',simulationTime,\
    #            'ultraSonicSensorLeft:',World.getSensorReading("ultraSonicSensorLeft"),\
    #            "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    # ##############################################
    # # Reasoning: figure out which action to take #
    # ##############################################
    # if simulationTime<5000:
    #     motorSpeed = dict(speedLeft=1, speedRight=1.5)
    # elif simulationTime<10000:
    #     motorSpeed = dict(speedLeft=-1.5, speedRight=-1.0)
    # elif simulationTime<15000:
    #     print ("Turning for a bit...",)
    #     World.execute(dict(speedLeft=2, speedRight=-2),15000,-1)
    #     print ("... got dizzy, stopping!")
    #     print ("BTW, nearest energy block is at:",World.getSensorReading("energySensor"))
    # else:
    #     motorSpeed = dict(speedLeft=0, speedRight=0)
        
    # ########################################
    # # Action Phase: Assign speed to wheels #
    # ########################################
    # # assign speed to the wheels
    # World.setMotorSpeeds(motorSpeed)
    # # try to collect energy block (will fail if not within range)
    # if simulationTime%10000==0:
    #     print ("Trying to collect a block...",World.collectNearestBlock())
