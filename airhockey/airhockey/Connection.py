import common
import socket
import vector
import time
import const

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
	
	if koordinates[0] < 0 or koordinates[0] > const.CONST.RobXMax or koordinates[1] < 0 or koordinates[1] > const.CONST.RobYMax:
	  print("!!!!!WARNING!!!!!! Koordinaten befinden sich ausserhalb des Spielfeldes")
	  return False
	"""
	connection = self.ConnectToSocket()
	if connection == None: 
	  return False
	"""
	
	try:
	  koordinateString = str(koordinates[0]) + ";" + str(koordinates[1])
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
    
    
        
        
        
class Strategy(common.Component):
  
    listens = ["strategy"]
    
    
    def __init__(self, eventhandler):
	super(Strategy, self).__init__(eventhandler)
	self.roboter=RobotConnection()
	self.oldRobotKoordinates = const.CONST.homePosition
  
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
	    if bag.puck.direction == {}:
	      return None
            direction = bag.puck.direction
        
        if direction[0] == 0:
	  #print("direction 0")
	  return None
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

        #Wenn Puck sich von Roboter entfernt bewege sich der Roboter vors Tor ansonsten auf dem Schnittpunkt des Puckes mit der x-Achse 0,1.
        koordinates = self.CrossXLine(bag, 0.1)
	
	robotKoordinates = self.calculateMovingPosition(koordinates)
	
	#sende Daten
	if self.roboter.SendKoordinatesToRoboter(robotKoordinates):
	  self.writeProtokoll(bag, robotKoordinates)
	  self.oldRobotKoordinates = robotKoordinates
	 

    def calculateMovingPosition(self, koordinates):
	if koordinates == None:
	  return None
	#print(koordinates)
	#Roboter braucht rund 0,6 Sekunden um sich in Bewegung zu setzen. Deshalb soll er sich nicht bewegen wenn der der Puck schneller ist
	if koordinates[2] > 4 or koordinates[2] < 0.6:
	  return None
	
	
	#Daten von Bild-Koordinatensystem ins Roboter-Koordinatensytem konvertieren
	xRob = (koordinates[0] * const.CONST.tableXMax) - const.CONST.durchmesserSchlaeger/2 + koordinates[0] * const.CONST.durchmesserSchlaeger
	#ueberpruefen ob Position innerhalb der Bewegungsgrenzen des Roboters liegt
	if xRob > const.CONST.RobXMax:
	  xRob = const.CONST.RobXMax
	if xRob < 0:
	  xRob = 0
	
	yRob = (koordinates[1] * const.CONST.tableYMax) - const.CONST.durchmesserSchlaeger/2 + koordinates[1] * const.CONST.durchmesserSchlaeger
	"""
	#Position auf unmittelbar vors Tor beschraenken
	Torgroesse = 200
	ymin = (const.CONST.RobYMax - Torgroesse) / 2.0
	ymax = (const.CONST.RobYMax + Torgroesse) / 2.0
	if yRob < ymin or yRob > ymax:
	  return None
	  """
	  
	
	#ueberpruefen ob Position innerhalb der Bewegungsgrenzen des Roboters liegt
	if yRob > const.CONST.RobYMax:
	  yRob = const.CONST.RobYMax
	if yRob < 0:
	  yRob = 0
	
	direction = vector.from_to(self.oldRobotKoordinates, [xRob,yRob])
	distance = vector.length(direction)
	"""
	Wenn die Bewegung zu klein ist, werden keine Koordianten gesendet um die Kommunikation mit Roboter gering zu halten,
	da fuer die Zeit der Bewegung der Roboter nicht ansprechbar ist
	"""
	if distance < const.CONST.minimumMovement:
	  return None
	
	"""
	Wenn der neue Punkt zu weit entfernt ist, wird dieser auf eine maximale Laenge gekuerzt, damit man evtl. neue 
	Richtungsaenderungen des Puckes schneller reagieren kann
	"""
	if distance > const.CONST.maximumMovement:
	  stepDirection = vector.mul_by(direction, 1.0 * const.CONST.maximumMovement / distance)
	  return vector.add(self.oldRobotKoordinates, stepDirection)
	
	return [xRob, yRob]
	
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