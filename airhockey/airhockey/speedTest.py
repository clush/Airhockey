import Connection
import time
import socket

def versuch(roboter, startpunkt, endpunkt):
  print(endpunkt)
  while not roboter.SendKoordinatesToRoboter(startpunkt):
    pass
  while not roboter.canMove():
    pass
  while not roboter.SendKoordinatesToRoboter(endpunkt):
    pass
  
  start = time.time()
  while not roboter.canMove():
    pass
  end =time.time()
  
  protokoll=open("speedtest.csv","a")
  protokoll.write(str(startpunkt[0]) + ";" + str(startpunkt[1]) + ";" + str(endpunkt[0]) + ";" + str(endpunkt[1]) + ";" + str(end - start) + "\n")
  protokoll.close()

def printzeile():
  protokoll=open("speedtest.csv","a")
  protokoll.write("\n")
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

for i in range(0,700,10):
  versuch(roboter, [0,0], [0,i])

printzeile()
printzeile()

for i in range (0,270,10):
  versuch(roboter, [0, 0], [i, 0])
"""
versuch(roboter, [0,0], [0,0])
versuch(roboter, [0,0], [0,100])
versuch(roboter, [0,0], [0,200])
versuch(roboter, [0,0], [0,300])
versuch(roboter, [0,0], [0,400])
versuch(roboter, [0,0], [0,500])
versuch(roboter, [0,0], [0,600])
versuch(roboter, [0,0], [0,690])
printzeile()

versuch(roboter, [100,0], [100,100])
versuch(roboter, [100,0], [100,200])
versuch(roboter, [100,0], [100,300])
versuch(roboter, [100,0], [100,400])
versuch(roboter, [100,0], [100,500])
versuch(roboter, [100,0], [100,600])
versuch(roboter, [100,0], [100,690])
printzeile()

versuch(roboter, [0,0], [100,0])
versuch(roboter, [0,0], [200,0])
versuch(roboter, [0,0], [260,0])
printzeile()

versuch(roboter, [0,350], [100,350])
versuch(roboter, [0,350], [200,350])
versuch(roboter, [0,350], [260,350])
printzeile()

versuch(roboter, [0,0], [100, 100])
versuch(roboter, [0,0], [150, 150])
versuch(roboter, [0,0], [200, 200])
versuch(roboter, [0,0], [250, 250])
printzeile()

versuch(roboter, [0,350], [100, 450])
versuch(roboter, [0,350], [150, 500])
versuch(roboter, [0,350], [200, 550])
versuch(roboter, [0,350], [250, 600])
printzeile()

"""