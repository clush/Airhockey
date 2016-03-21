 
 
class CONST:
    # TODO Config-File
    tableWidth = 795 #Breite des AirHockey-Tisches in mm
    # Y-Auslenkung
    tableDepth = 1400 #Tiefe des AirHockey-Tisches in mm
    # X-Auslenkung
    
    RobXMax = 260 # maximale X-Auslenkung des Roboters
    RobYMax = 690 # maximale Y-Auslenkung des Roboters
    #Robotergeschwindigkeit in x-Richtung
    RobVx = 1200
    #Robotergeschwindigkeit in Y-Richtung
    RobVy = 1200
    #Zeit die der Roboter benötigt um Befehl zu verarbeiten und sich in Bewegung zu setzen in Sekunden
    RobLatenzzeit = 0.05
    
    
    durchmesserPuck = 63 # Radius des Puckes in mm
    durchmesserSchlaeger = 95 #Radius des Schlaeger in mm
    
    tableXMax = tableDepth - durchmesserSchlaeger
    tableYMax = tableWidth - durchmesserSchlaeger 
    
    minimumMovement = 50
    maximumMovement = 690
    # Heimatposition des Roboters im Roboter-Koordinatensystem
    homePosition = [140, 400]
    
    
    
    
    # IP des Roboters
    roboterIP = "192.168.28.121"
    # Port auf dem der Roboter lauscht
    roboterPort = 1025
    # die Zeit die das Programm auf eine Antwort vom Roboter wartet. sollte mindestens die haelfte der framerate der Kamera sein
    timeoutTime = 1.0/100
    
    
    
    # Buffergroesse fuer die gespeicherten Puckpositionen zur Berechnung der Puckbahn
    DEFAULT_BUFFER_SIZE = 5

    # The acceptable difference between the next predicted and detected position
    # wird noch nicht verwendet
    ACCEPTABLE_PUCK_POSITION_DIFF = 100

    # The time in SECONDS for which the puck path should be predicted
    TABLE_BOUNDARIES_COLLISION_FORECAST_TIME = 0.5

    # The maximum amount of successive predictions
    MAX_SUCCESSIVE_PREDICTION_AMOUNT = 4
    
    
    
    
    # Bilderkennung
    # Hough parameters
    DP          = 1     # Inverse ratio of the accumulator resolution to the image resolution (keep at 1)
    MIN_DIS     = 10    # Minimum distance between the centers of the detected circles (in one frame)
    PARAM1      = 200   # Higher threshold passed to the Canny edge detector. The lower threshold is half the size of PARAM1
    PARAM2      = 30    # Accumulator threshold for the circle centers at the detection stage (the smaller it is, the more false circles)
    MIN_RADIUS  = 10    # Minimum circle radius
    MAX_RADIUS  = 20    # Maximum circle radius
    
    
    
    
    WINDOW_TITLE = 'Puckerkennung'
    
    
    #TODO Radius einberechnen
    yBorderBy0 = 0
    yBorderBy1 = 1
    xBorderBy0 = 0
    xBorderBy1 = 1