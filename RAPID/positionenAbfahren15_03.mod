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
VAR num x := 140;
VAR num y := 400;
VAR num z := 0;
VAR num found;
VAR bool okX;
VAR bool okY;
     
PROC main()

Target:=[[x,y,z],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
MoveL Target,v5000,fine,tool0\WObj:=Workobject_Table;
    
!SocketCreate server_socket;
!SocketBind server_socket, "192.168.28.121", 1025;
!SocketListen server_socket;


WHILE (TRUE) DO

SocketCreate my_socket;
SocketConnect my_socket,"192.168.28.222", 1025 \Time:=WAIT_MAX;
SocketReceive my_socket \Str:= receive_string \Time:=WAIT_MAX; 
SocketClose my_socket;
    
!SocketAccept server_socket, client_socket \ClientAddress:=client_ip \Time:=WAIT_MAX;
!Empfange Daten
!SocketReceive client_socket \Str := receive_string \Time:=WAIT_MAX;
!SocketClose client_socket;



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
IF NOT (okX OR okY) THEN
    ErrWrite \W, "Zeichenfolge konnte nicht in eine Zahl umgewandelt werden", "";
    GOTO abbrechen;
ENDIF

TPWrite " " \Num:=x;
TPWrite " " \Num:=y;

!Überprüfung, ob Koordinaten außerhalb des Spielfeldes liegen
IF (x<xMin) OR (x>xMax) OR (y<yMin) OR (y>yMax) THEN
    ErrWrite \W, "Gesendete Koordinaten liegen außerhalb des Spielfeldes", "";
    GOTO abbrechen;
ENDIF

!Bewegungsanweisung an Roboter
Target:=[[x,y,z],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
MoveL Target,vMax,fine,tool0\WObj:=Workobject_Table;


abbrechen:

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