import common
import socket
import vector
import time
import const
import math

class RobotConnection():

    
    
    def __init__(self):
        socket.setdefaulttimeout(const.CONST.timeoutTime)
        #self.connection = self.ConnectToSocket()
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.serversocket.bind(("192.168.28.222", 1025))
	#become a server socket
	self.serversocket.listen(1)
	self.isMoving = False
	while True:
	  try:
	    (self.clientsocket, self.address) = self.serversocket.accept()
	    break
	  except Exception:
	    pass
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
	self.serversocket.close()
    
    def __del__(self):
	self.serversocket.close()
    
    def ConnectToSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
	  #start = time.time()
	  s.connect((const.CONST.roboterIP, const.CONST.roboterPort))
	  #end = time.time()
	  #print("connectet")
	  #print(end - start)
	except Exception as e:
	  return None
	  #raise AirhockeyException("kann keine Verbindung aufbauen")
	return s
    
    def SendKoordinatesToRoboter(self, koordinates):
	if koordinates == None:
	  return False
	if not self.robCanReachPoint(koordinates):
	  print("!!!WARNING!!! Koordianten ausserhalb von Roboterreichweite.")
	  return False
	"""
	connection = self.ConnectToSocket()
	if connection == None: 
	  return False
	"""
	
	try:
	  koordinateString = str(round(koordinates[0],1)) + ";" + str(round(koordinates[1],1))
	  print(koordinateString)
	  sendData = self.clientsocket.send(koordinateString)
	  if sendData < len(koordinateString):
	      return False
	  self.isMoving = True
          return True
	except Exception as e:
	  return False
	
	"""
	
	connection = self.ConnectToSocket()
	if connection == None: 
	  return False
	
	#Daten senden
	koordinateString = str(koordinates[0]) + ";" + str(koordinates[1])
        try:
           sendData = connection.send(koordinateString)
	   connection.close()
           if sendData < len(koordinateString):
	      return False
	   
           return True
        except socket.timeout:
	   connection.close()
           return False
    """
    
    def canMove(self):
      if not self.isMoving:
	return True
      try:
	length = self.clientsocket.recv(1024)
	if length == 0:
	  return False
	self.isMoving = False
	return True
      except Exception:
	return False;
    
    def xmax(self,y):
      return round(math.sqrt(math.pow(532, 2) - math.pow(const.CONST.RobYMax / 2.0 - y, 2)) - 145, 1)
    
    def robCanReachPoint(self, point):
      if point == None:
	return False
      # Sofern sich das Ziel in der Mitte befindet, nehme die Maximalauslenkung der Mitte
      if abs(koordinates[1] - const.CONST.RobYMax / 2.0) < 1:
	  if koordinates[0] < 0 or koordinates[0] > const.CONST.RobXMaxMitte or koordinates[1] < 0 or koordinates[1] > const.CONST.RobYMax:
	    return False
	else:
	  if koordinates[0] < 0 or koordinates[0] > const.CONST.RobXMax or koordinates[1] < 0 or koordinates[1] > const.CONST.RobYMax:
	    return False
      return True  
        
class Strategy(common.Component):
  
    listens = ["strategy"]
    
    NULL = 0
    DEFEND = 1
    ANGRIFF1 = 2
    ANGRIFF2 = 3
    GOHOME = 4
    ANGRIFF3 = 5
    ANGRIFF4 = 6
    
    def __init__(self, eventhandler):
	super(Strategy, self).__init__(eventhandler)
	self.roboter=RobotConnection()
	self.oldRobotKoordinates = const.CONST.homePosition
	self.lastMove = self.NULL
  
    def MoveBetweenPuckAndGoal(self, bag):
        """
        calculates the point between Goal an puck with x Koordinates 0.1
        :param bag: The parameter bag.
        :return: point between Goal an puck with x Koordinates 0.1
        """
        positionGoal = [0, 0.5]
        directionGoalToPuck = vector.from_to(bag.puck.position, positionGoal)
        return self.CrossXLine(bag, 0.1, positionGoal, directionGoalToPuck)
       
    def CrossXLine(self,bag, xLine, startposition = None, direction = None):
        """
        calculates the crossing point of a line with x-koordinates xLine
        :param bag: The parameter bag.
        :param xLine: x-Value of the line [0..1]
        :param startposition: Position of the puck (if None the value from the bag is used)
        :param direction: movingdirection of the Puck(if None the value from the bag is used)
        :return: the crossing point of a line with x-koordinates xLine
        """        
        if startposition == None:
            startposition = bag.puck.position
        if direction == None:
            direction = bag.puck.direction
        """
        if direction[0] == 0:
	  #print("direction 0")
	  return None
	  """
        timeToCrossXLine = (xLine - startposition[0])/(direction[0] * bag.puck.velocity)
        yPosition = startposition[1] + timeToCrossXLine * direction[1] * bag.puck.velocity
        
        #print(timeToCrossXLine)
        #Wenn der Puck ausserhalb der Spielfeldbegrenzung liegt, wird dieser vor dem zurueckgeben noch an der Spielfeldgranze gespiegelt
        koordinates = vector.mirror_point_into_field([xLine, yPosition])
        return (koordinates[0], koordinates[1], timeToCrossXLine)
    
    def CrossYLine(self,bag, yLine, startposition = None, direction = None):
        """
        calculates the crossing point of a line with y-koordinates yLine
        :param bag: The parameter bag.
        :param yLine: y-Value of the line [0..1]
        :param startposition: Position of the puck (if None the value from the bag is used)
        :param direction: movingdirection of the Puck(if None the value from the bag is used)
        :return: the crossing point of a line with y-koordinates yLine
        """        
        if startposition == None:
          startposition = bag.puck.position
        if startposition == None:
	  return None
        if direction == None:
	  if bag.puck.direction == {}:
	    return None
          direction = bag.puck.direction
        if direction[1] == 0:
	  #print("direction 0")
	  return None
	
        timeToCrossYLine = (yLine - startposition[1])/(direction[1] * bag.puck.velocity)
        xPosition = startposition[0] + timeToCrossYLine * direction[0] * bag.puck.velocity
        
        
        #Wenn der Puck ausserhalb der Spielfeldbegrenzung liegt, wird dieser vor dem zurueckgeben noch an der Spielfeldgranze gespiegelt 
        koordinates = vector.mirror_point_into_field([xPosition, yLine])
        return (koordinates[0], koordinates[1], timeToCrossYLine)
      
    
              
    def handle_event_strategy(self, bag):
      #print(bag.puck.direction)
      
	if bag.is_table_setup:
	  return
	if not self.roboter.canMove():
	  return
	koordinates = self.decideStrategy(bag)
	
	
	#sende Daten
	if self.roboter.SendKoordinatesToRoboter(koordinates):
	  #self.writeProtokoll(bag, koordinates)
	  self.oldRobotKoordinates = koordinates
	  
    def gohome(self):
	self.lastMove = self.GOHOME
	return const.CONST.homePosition
	
    def attack1(self, robKoordinates):
	self.lastMove = self.ANGRIFF1
	return (0, robKoordinates[1])
    
    def attack2(self, bag):
	#alte Roboterkoordinaten ins Bildsystem umrechnen
	y = (self.oldRobotKoordinates[1] + const.CONST.durchmesserSchlaeger/2) / (const.CONST.tableYMax + const.CONST.durchmesserSchlaeger)
	koordinates = self.CrossYLine(bag, y)	
	robKoordinates = self.transformToRobotkoordinates(koordinates)
	if not self.roboter.robCanReachPoint(robKoordinates):
	  koordinates = self.CrossXLine(bag, 0.18)
	  robKoordinates = self.transformToRobotkoordinates(koordinates)
	if abs(self.calculateTimeToPoint(robKoordinates) - koordinates[2]) < 1.0/30:
	  self.lastMove = self.ANGRIFF2
	  #print(robKoordinates)
	  return robKoordinates
	return None
    
    def attack3(self,bag):
      return NotImplementedError
   
    def attack4(self, bag):
      return NotImplementedError
    
    def defend(self, bag):
	koordinates = self.CrossXLine(bag, 0.0)
	robKoordinates = self.transformToRobotkoordinates(koordinates)
	#Position auf unmittelbar vors Tor beschraenken
	Torgroesse = 200
	ymin = (const.CONST.RobYMax - Torgroesse) / 2.0
	ymax = (const.CONST.RobYMax + Torgroesse) / 2.0
	if robKoordinates[1] < ymin or robKoordinates[1] > ymax:
	  return None
	self.lastMove = self.DEFEND
	return robKoordinates
	
	
    def calculateTimeToPoint(self, koordinates):
	#Berechnet die Zeit die der Roboter benoetigt um die uebergebenen Koordinaten in 2 Schritten entlang der Achsen zu erreichen
	deltaX = abs(self.oldRobotKoordinates[0] - koordinates[0])
	deltaY = abs(self.oldRobotKoordinates[1] - koordinates[1])
	#ueberprüfen ob die delta groesser 0 sind, da sich der Roboter dann nicht in die se Richtung mehr bewegen muss
	if deltaX >= 1:
	  timeX = (deltaX + 163.23) / 1145.2
	else:
	  timeX = 0
	if deltaY >= 1:
	  timeY = (deltaY + 238.24) / 1579.13
	else:
	  timeY = 0
	return timeX + timeY
      
    def decideStrategy(self, bag):
	if self.lastMove == self.ANGRIFF2 or self.lastMove == self.ANGRIFF4:
	  return self.gohome()
	if not bag.puck.position[0] < 0.5:
	  if bag.puck.direction[0] < 0:
	    return self.defend(bag)
	  return self.gohome()
	#herausfinden ob Puck pendelt
	if abs(bag.puck.direction[0]) < 0.05:
	  if not self.lastMove == self.ANGRIFF3:
	    return self.attack3(bag)
	  return self.attack4(bag)
	puckDestination = self.CrossXLine(bag, 0.18)
	puckDestinationRobot = self.transformToRobotkoordinates(puckDestination)
	if self.lastMove == self.ANGRIFF1 and (abs(puckDestinationRobot[1] - self.oldRobotKoordinates[1]) < 50):
	  return self.attack2(bag)
	if self.calculateTimeToPoint(puckDestinationRobot) > puckDestination[3]:
	  return self.defend(bag)
	return self.attack1(puckDestinationRobot)
	
	  
      """
    def decideStrategy(self, bag):
	if bag.puck.position == {} or bag.puck.direction == {}:
	  return self.NULL
	
	#Wenn die letzte Bewegung der Angriffsschlag war, bewege dich zurueck vors Tor
	if self.lastMove == self.ANGRIFF2:
	  return self.GOHOME #evtl. Abfragen ob Puck schon wieder zurueckkommt
	
	#Wenn sich der Puck vom Roboter fortbewegt, soll er entweder nichts tun oder sich vors tor bewegen
	if bag.puck.position[0] < 0.2 and abs(bag.puck.direction[0]) < 0.01:
	  return self.ANGRIFF2
	
	if bag.puck.direction[0] >= 0:
	  if self.lastMove == self.ANGRIFF1:
	    return self.GOHOME
	  return self.NULL
	
	#Schnittpunkt einer Gerden etwa 20cm vorm Tor
	puckDestination = self.CrossXLine(bag, 0.18)
	puckDestinationRobot = self.transformToRobotkoordinates(puckDestination)
	
	#Wenn die letzte Bewegung, die Vorbereitung zum Angriff war und sich die berechneten Koordinaten weniger als 5cm (50mm) veraendert haben, greife an
	if (self.lastMove == self.ANGRIFF1) and (abs(puckDestinationRobot[1] - self.oldRobotKoordinates[1]) < 50):
	    return self.ANGRIFF2
	  
	#Wenn der Roboter den Puck in der Zeit erreichen kann bereite den Angriff vor
	if self.calculateTimeToPoint(puckDestination) < puckDestination[2]:
	  return self.ANGRIFF1
	  
	return self.DEFEND
	 """
    def transformToRobotkoordinates(self,koordinates):
	#Daten von Bild-Koordinatensystem ins Roboter-Koordinatensytem konvertieren
	if koordinates == None:
	  return None
	xRob = (koordinates[0] * const.CONST.tableDepth) - const.CONST.durchmesserSchlaeger/2 + koordinates[0] * const.CONST.durchmesserSchlaeger
	yRob = (koordinates[1] * const.CONST.tableWidth) - const.CONST.durchmesserSchlaeger/2 + koordinates[1] * const.CONST.durchmesserSchlaeger
	return (xRob, yRob)

    
	
    def writeProtokollWarning(self):
      protokoll=open("protokoll.txt","a")
      protokoll.write("!!!!!WARNING!!!!!! Koordinaten befinden sich ausserhalb des Spielfeldes\n")
      protokoll.close()
	
    def writeProtokoll(self, bag, koordinates):
      """if 'protokoll' not in bag:
	protokoll=open("protokoll.txt","w")
      else:"""
      protokoll=open("protokoll.txt","a")
      protokoll.write("aktuelle Roboterposition: "+ str(self.oldRobotKoordinates) + "; neue Roboterposition: " + str(koordinates) + "; Puckposition: " + str(bag.puck.position) +  "; Puckrichtung: " + str(bag.puck.direction) +"\n")
      protokoll.close()
	 #TODO Protokollfunktion niederschreiben der Koordinaten des Puktes, der Richtung, der position des Roboters und der berechneten Abfangposition
	 #TODO Roboter nicht komplett bewegen sondern, in kleineren Schritten. erhoeht die Korrigierbarkeit