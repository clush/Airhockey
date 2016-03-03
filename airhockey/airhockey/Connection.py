import common
import socket
import vector
import time

class RobotConnection():
    
    
    
    roboterIP = "192.168.28.121"
    roboterPort = 1025
    timeoutTime = 1.0/60
    
    tableWidth = 795 #Breite des AirHockey-Tisches in mm
    tableDepth = 1400 #Tiefe des AirHockey-Tisches in mm
    
    RobXMax = 250 #Tiefe
    RobYMax = 690 #Weite
    
    
    def __init__(self):
        socket.setdefaulttimeout(self.timeoutTime)
        #self.connection = self.ConnectToSocket()
        
    def ConnectToSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
	  start = time.time()
	  s.connect((self.roboterIP, self.roboterPort))
	  end = time.time()
	  print("connectet")
	  print(end - start)
	except Exception as e:
	  return None
	  #raise AirhockeyException("kann keine Verbindung aufbauen")
	return s
    
    def SendKoordinatesToRoboter(self, koordinates):
	connection = self.ConnectToSocket()
	if connection == None:
	  print("keine Verbindung") 
	  return False
	xRob = koordinates[0] * self.tableDepth
	if xRob > self.RobXMax:
	  xRob = self.RobXMax
	if xRob < 0:
	  xRob = 0
	
	yRob = koordinates[1] * self.tableWidth
	if yRob > self.RobYMax:
	  yRob = self.RobYMax
	if yRob < 0:
	  yRob = 0
	koordinateString = str(yRob) + ";" + str(xRob)
        try:
           sendData = connection.send(koordinateString)
           if sendData < len(koordinateString):
	      return False
	   connection.close()
           return True
        except socket.timeout:
	   connection.close()
           return False
    
    
    
        
        
        
class Strategy(common.Component):
  
    listens = ["strategy"]
    
    def __init__(self, eventhandler):
	super(Strategy, self).__init__(eventhandler)
	self.roboter=RobotConnection()
	self.oldKoordinates = [0, 0]
  
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
        yBorderBy0 = 0
        yBorderBy1 = 1
        if startposition == None:
            startposition = bag.puck.position
        if direction == None:
	    if bag.puck.direction == {}:
	      return None
            direction = bag.puck.direction
        
        if direction[0] == 0:
	  print("direction 0")
	  return None
        k = (xLine - startposition[0])/direction[0]
        yPosition = startposition[1] + k * direction[1]
        
        #Wenn der Puck ausserhalb der Spielfeldbegrenzung liegt, diesen solange an der Spielfeldbegrenzung spiegeln bis dieser innerhalb des Spielfeld liegt
        while (yPosition < yBorderBy0) or (yPosition > yBorderBy1):
	  if yPosition < yBorderBy0:
	      yPosition = yBorderBy0 -(yPosition - yBorderBy0)	     
	  if yPosition > yBorderBy1:
	      yPosition = yBorderBy1 -(yPosition - yBorderBy1)
	      
        return [xLine, yPosition]
    
    def CrossYLine(self,bag, yLine, startposition = None, direction = None):
        """
        calculates the crossing point of a line with y-koordinates yLine
        :param bag: The parameter bag.
        :param yLine: y-Value of the line [0..1]
        :param startposition: Position of the puck (if None the value from the bag is used)
        :param direction: movingdirection of the Puck(if None the value from the bag is used)
        :return: the crossing point of a line with y-koordinates yLine
        """
        
        xBorderBy0 = 0
        xBorderBy1 = 1
        
        if startposition == None:
          startposition = bag.puck.position
        if startposition == None:
	  return None
        if direction == None:
	  if bag.puck.direction == {}:
	    return None
          direction = bag.puck.direction
        if direction[1] == 0:
	  print("direction 0")
	  return None
	
        k = (yLine - startposition[1])/direction[1]
        xPosition = startposition[0] + k * direction[0]
        
        while (xPosition < xBorderBy0) or (xPosition > xBorderBy1):
	  if xPosition < 0:
	    xPosition = xPosition - (xBorderBy0 - xPosition)
	  if xPosition > 1:
	    xPosition = xPosition - (xBorderBy1 - xPosition)
           
        return [xPosition, yLine]
      
    
              
    def handle_event_strategy(self, bag):
	if bag.is_table_setup:
	  return
        #Roboter auf die Position bewegen auf die sich der Puck zu bewegt mit der x-Koordinate 0.1
        if (bag.puck.direction != {}) and (bag.puck.direction[0] >= 0):
	  koordinates = [0.1, 0.5] #Bewege dich vors Tor
	else:
	  koordinates = self.CrossXLine(bag, 0.1)
        #if not koordinates == None:
	#  self.roboter.SendKoordinatesToRoboter(koordinates)
	
	#print(koordinates)
	#koordinates = [0.1, bag.puck.position[1]]
	if not (koordinates == None) and (abs(vector.length(vector.from_to(koordinates, self.oldKoordinates))) > 0.05):
	  if self.roboter.SendKoordinatesToRoboter(koordinates):
	    self.oldKoordinates = koordinates