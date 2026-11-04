"""CoppeliaSim ZeroMQ adapter for DT8042 Lab 1 (Pioneer P3-DX).

Replaces the legacy Remote API implementation while preserving the
World.init/getSimulationTime/getSensorReading/setMotorSpeeds/execute/
collectNearestBlock interface used in the supplied Pioneer.py.

Start the supplied scene and its simulation in CoppeliaSim before calling init().
"""

import math
import random
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient


class EasyDict(dict):
    """Dictionary whose keys can also be read as attributes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


client = None
sim = None
robot = None
blockHandleArray = []
connectionTime = 0.0


def init():
    """Connect to CoppeliaSim and locate the robot, sensors and 12 blocks."""
    global client, sim, robot, blockHandleArray, connectionTime

    print("Program started")
    client = RemoteAPIClient()
    sim = client.require("sim")

    if sim.getSimulationState() == sim.simulation_stopped:
        raise RuntimeError("Start the simulation (Play) in CoppeliaSim before running Pioneer.py")

    left_motor = sim.getObject("/Pioneer_p3dx_leftMotor")
    right_motor = sim.getObject("/Pioneer_p3dx_rightMotor")
    pioneer = sim.getObject("/Pioneer_p3dx")
    left_sensor = sim.getObject("/Pioneer_p3dx_ultrasonicSensor3")
    right_sensor = sim.getObject("/Pioneer_p3dx_ultrasonicSensor5")

    robot = EasyDict(
        leftMotorHandle=left_motor,
        rightMotorHandle=right_motor,
        pioneerRobotHandle=pioneer,
        ultraSonicSensorLeft=left_sensor,
        ultraSonicSensorRight=right_sensor,
        energySensor=None,
    )

    # This scene contains two groups of similarly named objects.
    # The 12 collectible blocks are the original ConcretBlock#0..#11
    # (handles 6..17 in the inspected scene), NOT the later root-level
    # ConcretBlock[0..7] objects (handles 70..77), which are walls.
    # Explicitly choose the 12 verified paths rather than matching aliases.
    expected_paths = (
        [f"/Blocks/ConcretBlock[{i}]" for i in range(8)]
        + [f"/ConcretBlock[{i}]" for i in range(8, 12)]
    )
    block_handles = []
    for index, path in enumerate(expected_paths):
        try:
            handle = sim.getObject(path)
        except Exception as exc:
            raise RuntimeError(
                f"Missing expected energy block: {path}. "
                "Do not collect objects before verifying the scene layout."
            ) from exc
        actual_path = sim.getObjectAlias(handle, 1)
        if actual_path != path:
            raise RuntimeError(
                f"Unexpected object path for energy block {index}: "
                f"expected {path}, got {actual_path}"
            )
        block_handles.append((index, handle, path))

    blockHandleArray = []
    for index, (_, handle, _alias) in enumerate(block_handles):
        # Preserve the exercise's original setup: randomize the last five blocks.
        if index > 6:
            location = [random.random() * 6 - 1.5,
                        random.random() * 7 - 2.5,
                        0.0537]
            sim.setObjectPosition(handle, -1, location)
        position = sim.getObjectPosition(handle, -1)
        blockHandleArray.append([handle, index, position])

    connectionTime = sim.getSimulationTime()
    print(f"Connected to ZeroMQ Remote API. Found {len(blockHandleArray)} blocks.")
    print("Energy block paths:", ", ".join(expected_paths))
    return robot


def getSimulationTime():
    """Milliseconds elapsed since init(), matching the old World.py contract."""
    return int(round((sim.getSimulationTime() - connectionTime) * 1000))


def setMotorSpeeds(motorSpeed):
    """Set wheel angular target speeds (rad/s)."""
    sim.setJointTargetVelocity(robot.leftMotorHandle,
                               motorSpeed.get("speedLeft", 0))
    sim.setJointTargetVelocity(robot.rightMotorHandle,
                               motorSpeed.get("speedRight", 0))


def STOP():
    setMotorSpeeds(dict(speedLeft=0, speedRight=0))


def getSensorReading(sensor):
    """Read left/right sonar distance or nearest block distance and direction."""
    if sensor == "ultraSonicSensorLeft":
        h = robot.ultraSonicSensorLeft
    elif sensor == "ultraSonicSensorRight":
        h = robot.ultraSonicSensorRight
    elif sensor == "energySensor":
        nearest = findEnergyBlocks()
        if not nearest:
            return EasyDict(distance=float("inf"), direction=0.0)
        _, _, distance, direction = nearest[0]
        return EasyDict(distance=distance, direction=direction)
    else:
        print("Unknown sensor:", sensor)
        return None

    detected, distance, point, obj, normal = sim.readProximitySensor(h)
    if detected:
        return math.sqrt(sum(coord * coord for coord in point))
    return float("inf")


def robotDirection():
    orientation = sim.getObjectOrientation(robot.pioneerRobotHandle, -1)
    return normaliseAngle(math.pi / 2 - orientation[2])


def normaliseAngle(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def findEnergyBlocks():
    """Return block records sorted by increasing planar distance."""
    robot_pos = sim.getObjectPosition(robot.pioneerRobotHandle, -1)
    robot_direction = robotDirection()
    result = []
    for handle, index, _stored_position in blockHandleArray:
        # Read the CURRENT block location. A cached position can be stale
        # after a block is moved by the simulation or during troubleshooting.
        position = sim.getObjectPosition(handle, -1)
        dx = position[0] - robot_pos[0]
        dy = position[1] - robot_pos[1]
        distance = math.hypot(dx, dy)
        absolute_direction = math.atan2(dx, dy)
        direction = normaliseAngle(absolute_direction - robot_direction)
        result.append((handle, index, distance, direction))
    result.sort(key=lambda entry: entry[2])
    return result


def collectNearestBlock():
    nearest = findEnergyBlocks()
    if not nearest:
        return "No blocks nearby :("

    handle, index, distance, direction = nearest[0]
    if distance <= 0.5:
        # Safety check: only the 12 confirmed energy blocks may be moved.
        expected_path = (
            f"/Blocks/ConcretBlock[{index}]" if index < 8
            else f"/ConcretBlock[{index}]"
        )
        actual_path = sim.getObjectAlias(handle, 1)
        if actual_path != expected_path:
            raise RuntimeError(
                f"Refusing to collect non-energy object: {actual_path} "
                f"(expected {expected_path})"
            )
        removed_pos = [1000, 1000, -2]
        sim.setObjectPosition(handle, -1, removed_pos)
        blockHandleArray[index][-1] = removed_pos
        return "Energy collected :)"
    return "No blocks nearby :("


def debugEnergyDistances():
    """Print a one-shot comparison of cached and current distances.

    Call after World.init(), preferably with simulation paused and motors
    stopped. Does not change any CoppeliaSim object.
    """
    robot_pos = sim.getObjectPosition(robot.pioneerRobotHandle, -1)
    print("Robot XY:", [round(v, 3) for v in robot_pos[:2]])
    print("Loaded World module:", __file__)
    rows = []
    for handle, index, cached in blockHandleArray:
        path = sim.getObjectAlias(handle, 1)
        current = sim.getObjectPosition(handle, -1)
        cached_d = math.hypot(cached[0] - robot_pos[0],
                              cached[1] - robot_pos[1])
        actual_d = math.hypot(current[0] - robot_pos[0],
                              current[1] - robot_pos[1])
        rows.append((actual_d, cached_d, index, path))
    for actual_d, cached_d, index, path in sorted(rows):
        print(f"{actual_d:.2f} m (cached {cached_d:.2f} m) "
              f"| index={index} | {path}")
    return rows


def execute(motorSpeed, simulationTime, clockTime):
    """Run speeds until simulation-time limit (ms) or wall-time limit (s)."""
    start_sim = getSimulationTime()
    start_clock = time.monotonic()
    setMotorSpeeds(motorSpeed)
    try:
        while sim.getSimulationState() != sim.simulation_stopped:
            if simulationTime > 0 and getSimulationTime() >= start_sim + simulationTime:
                break
            if clockTime > 0 and time.monotonic() >= start_clock + clockTime:
                break
            time.sleep(0.05)
    finally:
            STOP()
