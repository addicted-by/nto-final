from client2server import client2server

class tracker:
    def run(tracklog):
        gamma = 0.85
        max_velocity = 1200

        last_timestamp = 0

        step_counter = 0
        c2s = client2server()
        status = c2s.getStatus()
        dx = int(status) & 0x0fff
        if dx > 2048:
                dx = dx - 4096

        previous_dx = dx
        previous_velocity = 0
        
    
        while True:        
            dx = int(status) & 0x0fff #0-12 bits
            state = (int(status) & 0xf000) >> 12 #12-15 bits
            '''
            Состояние радара:
            0 - неопределённое
            1 - отключен
            2 - включен
            3 - перемещается
            '''
            pos = (int(status) & 0xf0000) >> 16 #16-19 bits
            '''
            Положение радара:
            0 - неопределённое
            1 - поворачивается влево
            2 - поворачивается вправо
            3 - в крайнем левом положении
            4 - в крайнем правом положении
            '''
            time_stamp = (int(status) & 0x1ffff00000) >> 20 #20-36 bits
            '''
            Время в мс с начала работы
            '''
            if dx > 2048:
                dx = dx - 4096

            previous_dx = (dx if dx != -1536 else previous_dx)
            instant_velocity = (dx if pos != 3 and pos != 4 else (-1)**(2 if pos == 4 else 1) * 100)
            instant_velocity = (instant_velocity if dx != -1536 else previous_velocity)
            running_velocity = gamma * instant_velocity + (1 - gamma) * previous_velocity
            current_rotation_speed = int(100 / max_velocity * running_velocity)
            previous_velocity = running_velocity

            if last_timestamp != time_stamp:
                tracklog.write(f"Step number: {step_counter}\n".encode())
                tracklog.write(f"Time stamp: {time_stamp}\n".encode())
                tracklog.write(f"Bias: {dx}\n".encode())
                tracklog.write(f"State: {state}\n".encode())
                tracklog.write(f"Position: {pos}\n".encode())
                tracklog.write(f"Instant velocity: {instant_velocity}\n".encode())
                tracklog.write(f"Running velocity: {running_velocity}\n".encode())
                tracklog.write(f"Current rotation speed: {current_rotation_speed}\n".encode())
                last_timestamp = time_stamp
            #max velocity = 100, no_signal = -1536

            if abs(running_velocity) < max_velocity:
                if abs(running_velocity) < int(max_velocity/100):
                    status = c2s.moveStop()
                else:
                    if running_velocity > 0:
                        status = c2s.moveLeft(current_rotation_speed)
                    else:
                        status = c2s.moveRight(-1*current_rotation_speed)
            
            else:
                status = c2s.getStatus()

            step_counter += 1