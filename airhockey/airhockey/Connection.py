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
	start = time.time()
	self.connection = self.ConnectToSocket()
	if self.connection == None:
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
        try:
            #self.connection.send(str(xRob))
            
            """
	    try:
	      self.connection.recv(2048)
	    except socket.timeout:
	      pass
	    """
            self.connection.send(str(yRob))
            """
            while True:
	      try:
		self.connection.recv(2048)
		break
	      except socket.timeout:
		pass
            self.roboterIsMoving = True
            """
        except socket.timeout:
            pass
	self.connection.close()
	end = time.time()
	print(end - start)
	return True
    
    
    def CanMove(self):
        if not self.roboterIsMoving:
            return True
        try:
            self.connection.recv(2048)
            self.roboterIsMoving = False
            return True
        except socket.timeout:
            return False
        
        
        
class Strategy(common.Component):
  
    listens = ["strategy"]
    k_max = -1000
    
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
        positionGoal = [0,0.5]
        directionGoalToPuck = vector.from_to(bag.puck.position, positionGoal)
        return self.CrossXLine(bag, 0.1, positionGoal, directionGoalToPuck)
       
    def CrossXLine(self,bag, xLine, startposition = None, direction = None,):
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
        """
        print("x")
        print(startposition)
        print(direction)
        """
        
        if direction[0] == 0:
	  print("direction 0")
	  return None
        k = (xLine - startposition[0])/direction[0]
        #print(k)
        if k > 0:
            return self.MoveBetweenPuckAndGoal(bag)
	if k < self.k_max:
	  print("k zu klein")
	  return None
        yPosition = startposition[1] + k * direction[1]
        if yPosition < 0:
            hitpointBorder = self.CrossYLine(bag, 0, startposition, direction)
            return self.CrossXLine(bag, xLine, hitpointBorder, [direction[0], -direction[1]])
        if yPosition > 1:
            hitpointBorder = self.CrossYLine(bag, 1, startposition, direction)
            return self.CrossXLine(bag, xLine, hitpointBorder, [direction[0], -direction[1]])
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
	"""
	print("y")
        print(startposition)
        print(direction)
        """
        k = (yLine - startposition[1])/direction[1]
        #print(k)
        if k > 0:
            return self.MoveBetweenPuckAndGoal(bag)
	if k < self.k_max:
	  print("k zu klein")
	  return None
        xPosition = startposition[0] + k * direction[0]
        if xPosition < 0:
            hitpointBorder = self.CrossXLine(bag, 0, startposition, direction)
            return self.CrossYLine(bag, yLine, hitpointBorder, [-direction[0], direction[1]])
        if xPosition > 1:
            hitpointBorder = self.CrossXLine(bag, 1, startposition, direction)
            return self.CrossYLine(bag, yLine, hitpointBorder, [-direction[0], direction[1]])
        return [xPosition, yLine]
      
    
              
    def handle_event_strategy(self, bag):
	if bag.is_table_setup:
	  return
	"""
        if not roboter.CanMove():
            return
        """
        #Roboter auf die Position bewegen auf die sich der Puck zu bewegt mit der x-Koordinate 0.1
        
        koordinates = self.CrossXLine(bag, 0.1)
        #if not koordinates == None:
	#  self.roboter.SendKoordinatesToRoboter(koordinates)
	
	print(koordinates)
	#koordinates = [0.1, bag.puck.position[1]]
	if not (koordinates == None) and (abs(vector.length(vector.from_to(koordinates, self.oldKoordinates))) > 0.05):
	  if self.roboter.SendKoordinatesToRoboter(koordinates):
	    self.oldKoordinates = koordinates