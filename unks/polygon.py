from client2server import client2server
from matplotlib import pyplot as plt


class Polygon:
    def run(self, track_file):
        c2s = client2server()
        track_file.write(f"Obstacles positions {c2s.obstacles_positions}\n")
        radar_positions = []
        satellite_positions = []
        for current_status in c2s.iterate():
            radar_positions.append(c2s.radar.current_position)
            satellite_positions.append(c2s.satellite.current_position)
            dx = current_status[0]
            state = current_status[1]
            pos = current_status[2]
            time_stamp = current_status[3]

            track_file.write(f"dx = {dx}, state = {state}, pos_state = {pos}, ts = {time_stamp}\n")
            print(f"Current position {c2s.radar.current_position}")
            if dx > 2048:
                dx = dx - 4096
            if abs(dx) < 500:
                if abs(dx) < 10:
                    c2s.moveStop()
                else:
                    if dx > 0:
                        print("Move left")
                        c2s.moveLeft(4)
                    else:
                        print("Move right")
                        c2s.moveRight(4)

        return radar_positions, satellite_positions, c2s.obstacles_positions


if __name__ == "__main__":
    polygon = Polygon()
    log_file = open("log.txt", "w")
    radar_positions, satellite_positions, obstacles_positions = polygon.run(log_file)
    log_file.close()
    steps_number = len(radar_positions)

    plt.plot(range(steps_number), radar_positions, label="radar trajectory")
    plt.plot(range(steps_number), satellite_positions, label="satellite trajectory")
    for idx in range(0, len(obstacles_positions), 2):
        left_bound = obstacles_positions[idx]
        right_bound = obstacles_positions[idx + 1]
        plt.fill_between(
            [0, steps_number],
            [left_bound, left_bound],
            [right_bound, right_bound],
            alpha=0.2,
            color="black"
        )
    plt.legend()
    plt.savefig("log_plot.png")
