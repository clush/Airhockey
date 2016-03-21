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




protokoll=open("speedtest.csv","w")
protokoll.write("xStart;yStart;xEnde;yEnde;Zeit\n")
protokoll.close()
roboter=Connection.RobotConnection()
print("Server open")

for i in range(0,700,10):
  versuch(roboter, [130,0], [130,i])

for i in range (0,270,10):
  versuch(roboter, [0, 172], [i, 172])
  

"""
for i in range(0,700,10):
  versuch(roboter, [260,0], [260,i])

printzeile()
printzeile()

for i in range (0,270,10):
  versuch(roboter, [0, 345], [i, 345])
  
  
printzeile()
printzeile()

for i in range(0, 270, 10):
  versuch(roboter, [0, 0], [i, i])

printzeile()
printzeile()

for i in range(0, 270, 10):
  versuch(roboter, [0, 350], [i, 350 + i])
"""
