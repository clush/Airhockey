import Connection
import time
import socket

def versuch(roboter, startpunkt, endpunkt):
  while not roboter.SendKoordinatesToRoboter(startpunkt):
    pass
  print("test1")
  while not roboter.SendKoordinatesToRoboter(endpunkt):
    pass
  print("test2")
  start = time.time()
  while not roboter.SendKoordinatesToRoboter(endpunkt):
    pass
  end = time.time()
  print("test3\n")
  protokoll=open("speedtest.csv","a")
  protokoll.write(str(startpunkt[0]) + ";" + str(startpunkt[1]) + ";" + str(endpunkt[0]) + ";" + str(endpunkt[1]) + ";" + str(end - start) + "\n")
  protokoll.close()




"""
start= time.time()
#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind((socket.gethostname(), 1025))
#become a server socket
serversocket.listen(5)
serversocket.close()
end=time.time()
print(str(end-start))
"""
roboter = Connection.RobotConnection()
while 1:
  while not raw_input():
    pass
  roboter.SendKoordinatesToRoboter([0,0])
  while not raw_input():
    pass
  print("sende")
  roboter.SendKoordinatesToRoboter([200,0])
  print("gesendet")
"""
protokoll=open("speedtest.csv","w")
protokoll.write("xStart;yStart;xEnde;yEnde;Zeit\n")
protokoll.close()
roboter=Connection.RobotConnection()
print("Server open")
versuch(roboter, [0,0], [0,0])
versuch(roboter, [0,0], [0,100])
versuch(roboter, [0,0], [0,200])
versuch(roboter, [0,0], [0,300])
versuch(roboter, [0,0], [0,400])
versuch(roboter, [0,0], [0,500])
versuch(roboter, [0,0], [0,600])
versuch(roboter, [0,0], [0,690])


versuch(roboter, [100,0], [100,100])
versuch(roboter, [100,0], [100,200])
versuch(roboter, [100,0], [100,300])
versuch(roboter, [100,0], [100,400])
versuch(roboter, [100,0], [100,500])
versuch(roboter, [100,0], [100,600])
versuch(roboter, [100,0], [100,690])

versuch(roboter, [0,0], [100,0])
versuch(roboter, [0,0], [200,0])
versuch(roboter, [0,0], [260,0])

versuch(roboter, [0,350], [100,350])
versuch(roboter, [0,350], [200,350])
versuch(roboter, [0,350], [260,350])

versuch(roboter, [0,0], [100, 100])
versuch(roboter, [0,0], [150, 150])
versuch(roboter, [0,0], [200, 200])
versuch(roboter, [0,0], [250, 250])

versuch(roboter, [0,350], [100, 450])
versuch(roboter, [0,350], [150, 500])
versuch(roboter, [0,350], [200, 550])
versuch(roboter, [0,350], [250, 600])
"""

