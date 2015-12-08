import common
import socket
import vector

class RobotConnection(common.Component):
    
    listens = ["datatransfer"]
    
    roboterIP = ""
    roboterPort = 1025
    timeoutTime = 1e-5
    
    
    def __init__(self, eventhandler):
        super(connection, self).__init__(eventhandler)
        socket.setdefaulttimeout(self.timeoutTime)
        self.connection = connectToSocket()
        
    def ConnectToSocket(self):
        pass
        #TODO connection
    
    def SendKoordinatesToRoboter(self, koordinates):
        try:
            self.connection.send(str(self.koordinates[0]))
            self.connection.recv(2048)
            self.connection.send(str(self.koordinates[1]))
            self.connection.recv(2048)
            self.roboterCanMove = False
        except socket.timeout:
            pass
        
    def RoboterReachedPosition(self):
        if self.roboterCanMove:
            return
        try:
            self.connection.recv(2048)
            self.roboterCanMove = True
        except socket.timeout:
            pass
        
    def MoveBetweenPuckAndGoal(self, bag):
        """
        calculates the point between Goal an puck with x Koordinates 0.1
        :param bag: The parameter bag.
        :return: point between Goal an puck with x Koordinates 0.1
        """
        positionGoal = [0,0.5]
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
        k = (xLine - startposition[0])/direction[0]
        if k < 0:
            return self.MoveBetweenPuckAndGoal(bag)
        yPosition = startposition[1] + k * direction[1]
        if yPosition < 0:
            hitpointBorder = self.CrossYLine(bag, 0, startposition, direction)
            return self.CrossXLine(bag, xLine, hitpointBorder, [direction[0], -direction[1]])
        if yPosition > 1:
            hitpointBorder = self.CrossYLine(bag, 1, startposition, direction)
            return self.CrossXLine(bag, xLine, hitpointBorder, [direction[0], -direction[1]])
        return [xLine, yPosition]
    
    def CrossYLine(self,bag, xLine, startposition = None, direction = None):
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
        if direction == None:
            direction = bag.puck.direction
        k = (yLine - startposition[1])/direction[1]
        if k < 0:
            return self.MoveBetweenPuckAndGoal(bag)
        xPosition = startposition[0] + k * direction[0]
        if xPosition < 0:
            hitpointBorder = self.CrossXLine(bag, 0, startposition, direction)
            return self.CrossYLine(bag, yLine, hitpointBorder, [-direction[0], direction[1]])
        if xPosition > 1:
            hitpointBorder = self.CrossXLine(bag, 1, startposition, direction)
            return self.CrossYLine(bag, yLine, hitpointBorder, [-direction[0], direction[1]])
        return [xPosition, yLine]
              
    def handle_event_datatransfer(self, bag):
        self.RoboterReachedPosition()
        if not self.roboterCanMove:
            return
        #Roboter auf die Position bewegen auf die sich der Ouck zu bewegt mit der x-Koordinate 0.1
        koordinates = self.CrossXLine(bag, 0.1)
        self.SendKoordinatesToRoboter(koordinates)