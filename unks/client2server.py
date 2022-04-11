import numpy as np
from bisect import bisect_right

SPACE_LENGTH = 1000
TOTAL_STEPS = 1000
MAX_OBSTACLE_LEN = 50
OBSTACLES_NUMBER_PROBA = 0.4
STEPS_NUMBER_PROBA = 0.4
SPEED_STD = 10


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
        if self.current_position >= SPACE_LENGTH:
            self.current_position = SPACE_LENGTH
            self.position_state = RadarPositionState.EXTREME_RIGHT
        elif self.current_position <= -SPACE_LENGTH:
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
    MAX_SPEED = 5

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


class client2server:
    def __init__(self):
        self.radar = Radar()
        self.satellite = Satellite()
        self.timestamp = 0
        self.log_file = open("c2s_log.txt", "w")

        number_of_obstacles = np.random.geometric(p=OBSTACLES_NUMBER_PROBA)
        left_obstacles = np.random.uniform(-SPACE_LENGTH, -MAX_OBSTACLE_LEN, size=number_of_obstacles // 2 * 2)
        right_obstacles = np.random.uniform(MAX_OBSTACLE_LEN, SPACE_LENGTH, size=number_of_obstacles // 2 * 2)
        left_obstacles.sort()
        right_obstacles.sort()
        self.obstacles_positions = np.concatenate([left_obstacles, right_obstacles])
        self.log_file.write(f"Obstacles positions {self.obstacles_positions}\n")

    def getStatus(self):
        dx = self.satellite.current_position - self.radar.current_position
        if abs(dx) > self.radar.VIEW:
            dx = -1516

        between_obstacles_position = bisect_right(self.obstacles_positions, self.satellite.current_position)
        if 0 < between_obstacles_position < len(self.obstacles_positions):
            # even indices in self.obstacles_positions -- left corners of obstacles
            # odd indices in self.obstacles_positions -- right corners of obstacles
            if between_obstacles_position % 2 == 1:
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

    def iterate(self):
        number_of_steps = 0
        for self.timestamp in range(TOTAL_STEPS):
            if number_of_steps == 0:
                number_of_steps = np.random.geometric(p=STEPS_NUMBER_PROBA)
                speed = np.round(np.random.normal(loc=0, scale=SPEED_STD))
                self.log_file.write(f"Number of satellite steps {number_of_steps} with speed {speed}\n")
            number_of_steps -= 1
            self.satellite.step(speed)
            yield self.getStatus()

