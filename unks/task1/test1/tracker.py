from client2server import client2server

class tracker:
  def run(tracklog):
      c2s = client2server()
      while True:
          status = c2s.getStatus()
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

          tracklog.write(f"Bias: {dx}".encode())
          tracklog.write(f"State: {state}".encode())
          tracklog.write(f"Position: {pos}".encode())
          tracklog.write(f"Time stamp: {time_stamp}".encode())
          
          # * в крайнем левом + неопределенное (состояние) -- вправо на 10
          # * в крайнем правом + неопределенное (состояние) -- влево на 10
          # ! поворачивается влево + dx < 0 -- вправо на 5
          # ! поворачивается вправо + dx > 0 -- влево на 5
          # ? (2) поворачивается вправо + неопределенное (состояние или положение) -- влево на 10
          # ? (2) поворачивается влево + неопределенное (состояние или положение) -- вправо на 10
          # time_stamp неопределенное (положение или состояние) типо преграда
          if pos == 3:
              c2s.moveRight(10)
          if pos == 4:
              c2s.moveLeft(10)
          if pos == 0 or state == 0:
              tracklog.write(f"Pos: {pos} " + f"\nState: {state} " + 
                                f"\nTime stamp: {time_stamp}")
          if abs(dx) < 1000:
              if abs(dx) < 5:
                  c2s.moveStop()
              else:
                  if dx > 0:
                      c2s.moveLeft(5)
                  else:
                      c2s.moveRight(5)
