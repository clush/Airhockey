MODULE positionenAbfahren    
    
VAR socketdev server_socket;
VAR socketdev client_socket;
VAR socketdev my_socket;
VAR string receive_string;
VAR string client_ip;
VAR string partX;
VAR string partY;
VAR robtarget Target;
VAR num count;
VAR num x := 0;
VAR num y := 345;
VAR num z := 0;
VAR num found;
VAR num xMaxV;
VAR bool okX;
VAR bool okY;



     
PROC main()

Target:=[[x,y,z],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
MoveL Target,v5000,fine,tool0\WObj:=Workobject_Table;
    
SocketCreate my_socket;
SocketConnect my_socket,"192.168.28.222", 1025 \Time:=WAIT_MAX;


WHILE (TRUE) DO

!Empfange Daten
SocketReceive my_socket \Str:= receive_string \Time:=WAIT_MAX; 

found := StrFind(receive_string,1,";");

IF (found>StrLen(receive_string)) THEN
    ErrWrite \W, "Trennzeichen nicht gefunden","Koordinten müssen durch ; getrennt werden"; 
    GOTO abbrechen;
ENDIF

!Auslesen der Koordinten als String
partX := StrPart(receive_string,1,found-1);
partY := StrPart(receive_string,found+1,StrLen(receive_string)-found);

!Convertieren in Zahlen
okX := StrToVal(partX,x);
okY := StrToVal(partY,y);

!Überprüfung, ob Convertierung funktioniert hat
IF NOT (okX AND okY) THEN
    ErrWrite \W, "Zeichenfolge konnte nicht in eine Zahl umgewandelt werden", "";
    GOTO abbrechen;
ENDIF

TPWrite " " \Num:=x;
TPWrite " " \Num:=y;

!Überprüfung, ob Koordinaten außerhalb des Spielfeldes liegen
IF abs(y-345)<1 THEN 
    xMaxV:= xMaxMitte;
ELSE
    xMaxV:= xMax;
ENDIF

IF (x<xMin) OR (x>xMaxV) OR (y<yMin) OR (y>yMax) THEN 
    ErrWrite \W, "Gesendete Koordinaten liegen außerhalb des Spielfeldes" , receive_string;
    GOTO abbrechen;
ENDIF

!Bewegungsanweisung an Roboter
Target:=[[x,y,z],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
MoveL Target,vMax,fine,tool0\WObj:=Workobject_Table;


abbrechen:
SocketSend my_socket \Str:="Ready";

ENDWHILE


ERROR
RETRY;
UNDO
!SocketClose server_socket;
!SocketClose client_socket;
SocketClose my_socket;

	ENDPROC
    
	PROC Jump_Home()
        MoveL Target_Home,v50,fine,tool0\WObj:=wobj0;
    ENDPROC
    
    PROC Kalibrierungstest()
	    MoveL Target_10,v50,fine,tool0\WObj:=Workobject_Table;
        MoveL Target_20,v50,fine,tool0\WObj:=Workobject_Table;
        MoveL Target_30,v50,fine,tool0\WObj:=Workobject_Table; 
        MoveL Target_40,v50,fine,tool0\WObj:=Workobject_Table; 
        
	ENDPROC
    
    
    
ENDMODULE