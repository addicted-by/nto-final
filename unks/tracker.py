import numpy as np

SPACE_LENGTH = 1000
TOTAL_STEPS = 5000

OBSTACLES_NUMBER_PROBA = 0.1
STEPS_NUMBER_PROBA = 0.4
SPEED_STD = 10

number_of_obstacles = np.random.geometric(p=OBSTACLES_NUMBER_PROBA)
obstacles_positions = np.round(np.random.uniform(low=-SPACE_LENGTH, high=SPACE_LENGTH, size=number_of_obstacles))
obstacles_positions.sort()


class RadarState:
    UNDEFINED = 0
    OFF = 1
    ON = 2
    MOVING = 3


class RadarPositionState:
    UNDEFINED = 0
    TURNS_LEFT = 1
    TURNS_RIGHT = 2
    EXTREME_LEFT = 3
    EXTREME_RIGHT = 4


class Radar:
    MAX_SPEED = 10
    VIEW = 100

    def __init__(self):
        self.state = RadarState.ON
        self.position_state = RadarPositionState.UNDEFINED
        self.current_position = 0

    def moveStop(self):
        if self.current_position <= SPACE_LENGTH:
            self.current_position = SPACE_LENGTH
            self.position_state = RadarPositionState.EXTREME_RIGHT
        elif self.current_position >= -SPACE_LENGTH:
            self.current_position = -SPACE_LENGTH
            self.position_state = RadarPositionState.EXTREME_LEFT
        else:
            self.position_state = RadarPositionState.UNDEFINED

    def moveLeft(self, speed: int):
        speed = min(Radar.MAX_SPEED, speed)
        self.current_position = min(SPACE_LENGTH, self.current_position + speed)
        if self.current_position >= SPACE_LENGTH:
            self.position_state = RadarPositionState.EXTREME_RIGHT
        else:
            self.position_state = RadarPositionState.TURNS_RIGHT

    def moveRight(self, speed: int):
        speed = min(Radar.MAX_SPEED, speed)
        self.current_position = max(-SPACE_LENGTH, self.current_position - speed)
        if self.current_position <= -SPACE_LENGTH:
            self.position_state = RadarPositionState.EXTREME_LEFT
        else:
            self.position_state = RadarPositionState.TURNS_LEFT


class Satellite:
    MAX_SPEED = 20

    def __init__(self):
        self.current_position = 0

    def step(self, speed: int):
        if speed > Satellite.MAX_SPEED:
            speed = Satellite.MAX_SPEED
        if speed < -Satellite.MAX_SPEED:
            speed = -Satellite.MAX_SPEED
        self.current_position += speed
        self.current_position = min(SPACE_LENGTH, self.current_position)
        self.current_position = max(-SPACE_LENGTH, self.current_position)


class Tracker:
    def __init__(self):
        self.radar = Radar()
        self.satellite = Satellite()
        self.timestamp = 0

    def getStatus(self):
        self.timestamp += 1
        dx = self.radar.current_position - self.satellite.current_position
        if abs(dx) > self.radar.VIEW:
            dx = -1516
        state = self.radar.state
        position_state = self.radar.position_state
        timestamp = self.timestamp

        return dx, state, position_state, timestamp

    def moveStop(self):
        self.radar.moveStop()

    def moveLeft(self, speed: int):
        self.radar.moveLeft(speed)

    def moveRight(self, speed: int):
        self.radar.moveRight(speed)

