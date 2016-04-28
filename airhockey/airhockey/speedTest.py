import Connection
import time
import socket
import math
import const

def versuch(roboter, startpunkt, endpunkt):
  print(endpunkt)
  while not roboter.SendKoordinatesToRoboter(startpunkt):
    pass
  while not roboter.canMove():
    pass
  start = time.time()
  while not roboter.SendKoordinatesToRoboter(endpunkt):
    pass   
  while not roboter.canMove():
    pass
  end =time.time()
  
  #protokoll=open("speedtest.csv","a")
  protokoll.write(str(startpunkt[0]) + ";" + str(startpunkt[1]) + ";" + str(endpunkt[0]) + ";" + str(endpunkt[1]) + ";" + str(end - start) + "\n")
  #protokoll.close()

def printzeile():
  #protokoll=open("speedtest.csv","a")
  protokoll.write("\n")
  #protokoll.close()

#def xmax(y):
 # return math.sqrt(math.pow(532, 2) - math.pow(const.CONST.RobYMax / 2.0 - y, 2)) - 145


protokoll=open("speedtest.csv","w")
protokoll.write("xStart;yStart;xEnde;yEnde;Zeit\n")
#protokoll.close()

roboter=Connection.RobotConnection()
print("Server open")
messungen = [90, 180, 390, 510, 540, 630]

for y in messungen:
  protokoll.write("Bewegung bei y=" + str(y) + "\n")
  for x in range(0, 270, 10):
    versuch(roboter, [0, y], [x, y])
    #print(i)
    while not roboter.canMove():
      pass
  protokoll.write("\n\n")

"""
for x in range(0, 386, 10):
  versuch(roboter, [0, 345], [x, 345])
  while not roboter.canMove():
      pass
"""

protokoll.close()
