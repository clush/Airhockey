MODULE CalibData
    CONST num xMin:=0;
    CONST num xMax:= 260;
    CONST num xMaxMitte:=386;
    CONST num yMin:= 0;
    CONST num yMax:= 690;    
	TASK PERS wobjdata Workobject_Table:=[FALSE,TRUE,"",[[0,0,0],[1,0,0,0]],[[423.6,-349.4,294.7],[1,0,0,0]]];      
    CONST robtarget Target_10:=[[xMin,yMin,30],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    CONST robtarget Target_20:=[[xMin,yMax,30],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]]; 
    CONST robtarget Target_30:=[[xMax,yMax,30],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    CONST robtarget Target_40:=[[xMax,yMin,30],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]]; 
    CONST robtarget Target_Home:=[[453,26,610],[0,1,0,0],[-1,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
ENDMODULE