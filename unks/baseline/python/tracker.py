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

          tracklog.write(f"{dx}".encode())
          tracklog.write(f"{state}".encode())
          tracklog.write(f"{pos}".encode())
          tracklog.write(f"{time_stamp}".encode())
          
          if abs(dx) < 1000:
              if abs(dx) < 5:
                  c2s.moveStop()
              else:
                  if dx > 0:
                      c2s.moveLeft(5)
                  else:
                      c2s.moveRight(5)
