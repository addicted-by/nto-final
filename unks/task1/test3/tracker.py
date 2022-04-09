from client2server import client2server

class tracker:
  def run(tracklog):
      c2s = client2server()
      i = 0
      while i == 0:
          status = c2s.getStatus()
          dx = int(status) & 0x0fff
          if dx > 2048:
              dx = dx - 4096
          # tracklog.write(f"{dx}".encode())
          if abs(dx) < 500:
              if abs(dx) < 10:
                  c2s.moveStop()
              else:
                  if dx > 0:
                      c2s.moveLeft(4)
                  else:
                      c2s.moveRight(4)
