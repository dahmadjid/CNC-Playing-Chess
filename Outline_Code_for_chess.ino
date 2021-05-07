#include <AccelStepper.h>
#include <Servo.h>
#include <string.h>

int stepsperrev,MAX,SPEED1=0,SPEED2=0,SPEED3=0,lot,coefs,CLOSE,OPEN,NUMSTP3,p1,p2,p3,BT;
int ENDSTOP1,ENDSTOP2,ENDSTOP3,pic,POS1,POS2,CALC1,CALC2,d1,d2,d3,Y1=8,a=0,OUT=-2,b=0;
String STRN,STR2;
AccelStepper stepperx(1,2,5);  
AccelStepper steppery(1,3,6);
AccelStepper stepperz(1,4,7);


Servo servo;// for chess only , in other programs we're going to have them connected individually 
struct{
int x;
int y;
}typedef Coordinates;


 
Coordinates inipoint={0,0};
Coordinates dpoint={0,0};
Coordinates dpointf={0,0};
Coordinates kpoint={0,0};
Coordinates kpointf={0,0};
Coordinates rpoint={0,0};
Coordinates rpointf={0,0};
Coordinates epoint1={0,0};
Coordinates epoint2={0,0};
Coordinates epointf={0,0};
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void MOVE(Coordinates despoint,Coordinates despointf){
  SPEED1=0;
  SPEED2=0;
 //microstepping
 //THE MULTISTEPPER LIBRARY IS FUCKING AMAZING
d1=(despoint.x)*lot*coefs;
d2=(despoint.y)*lot*coefs;
POS1=stepperx.currentPosition();
POS2=steppery.currentPosition();
SPEED1=(d1>POS1)?SPEED1:(-SPEED1);
SPEED2=(d2>POS2)?SPEED2:(-SPEED2);

while(stepperx.currentPosition()!=d1 || steppery.currentPosition()!=d2 ){
  if(stepperx.currentPosition()!=d1){
   
    stepperx.setSpeed(SPEED1);
  stepperx.runSpeed();
  
  }
  if(steppery.currentPosition()!=d2){
    steppery.setSpeed(SPEED2);
steppery.runSpeed();
  }
  /* WE CAN USE A millis() TO MAKE ALL 3 STEPPERS GO AT THE SAME TIME WITH A SLIGHT DELAY FOR THE 3RD STEPPER*/
}


 
d3=NUMSTP3;
while(stepperz.currentPosition()!=d3){
stepperz.setSpeed(SPEED3);
stepperz.runSpeed();

}

servo.write(CLOSE);
while(stepperz.currentPosition()!=0){
stepperz.setSpeed(-SPEED3);
stepperz.runSpeed();

}

SPEED1=(SPEED1>0)?SPEED1:-SPEED1;
SPEED2=(SPEED2>0)?SPEED2:-SPEED2;
 d1=(despointf.x)*lot*coefs;
 d2=(despointf.y)*lot*coefs;
POS1=stepperx.currentPosition();
POS2=steppery.currentPosition();
SPEED1=(d1>POS1)?SPEED1:(-SPEED1);
SPEED2=(d2>POS2)?SPEED2:(-SPEED2);

while(stepperx.currentPosition()!=d1 || steppery.currentPosition()!=d2 ){
  if(stepperx.currentPosition()!=d1){
    
    stepperx.setSpeed(SPEED1);
  stepperx.runSpeed();
  
  }
  if(steppery.currentPosition()!=d2){
    steppery.setSpeed(SPEED2);
steppery.runSpeed();
  }
}



  //x is an the length of the arm
 d3=NUMSTP3;
while(stepperz.currentPosition()!=d3){
stepperz.setSpeed(SPEED3);
stepperz.runSpeed();

}


servo.write(OPEN);
while(stepperz.currentPosition()!=0){
stepperz.setSpeed(-SPEED3);
stepperz.runSpeed();

}
SPEED1=(SPEED1>0)?SPEED1:-SPEED1;
SPEED2=(SPEED2>0)?SPEED2:-SPEED2;

 d1=0;
d2=0;
POS1=stepperx.currentPosition();
POS2=steppery.currentPosition();
SPEED1=(d1>POS1)?SPEED1:(-SPEED1);
SPEED2=(d2>POS2)?SPEED2:(-SPEED2);

while(stepperx.currentPosition()!=d1 || steppery.currentPosition()!=d2 ){
  if(stepperx.currentPosition()!=d1){
    
    stepperx.setSpeed(SPEED1);
  stepperx.runSpeed();
  
  }
  if(steppery.currentPosition()!=d2){
    
    steppery.setSpeed(SPEED2);
steppery.runSpeed();
  }
}
if(STRN[4]=="m"){
Serial.print('1');
}
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////
void INI2(){
    SPEED1=0;
  SPEED2=0;
  SPEED1=(SPEED1>0)?SPEED1:-SPEED1;
SPEED2=(SPEED2>0)?SPEED2:-SPEED2;
while(ENDSTOP2!=1 || ENDSTOP1!=1 ){
  if(ENDSTOP1!=1){
   stepperx.setSpeed(-SPEED1);
  stepperx.runSpeed();
  }
  if(ENDSTOP2!=1){
     
 steppery.setSpeed(-SPEED2);
  steppery.runSpeed();

  }
}
while(ENDSTOP3!=1){
stepperz.setSpeed(-SPEED3);
stepperz.runSpeed();
}
d1=CALC1;
d2=CALC2;
while(stepperx.currentPosition()!=d1 || steppery.currentPosition()!=d2 ){
  if(stepperx.currentPosition()!=d1){
    stepperx.setSpeed(SPEED1);
  stepperx.runSpeed();
  
  }
  if(steppery.currentPosition()!=d2){
    steppery.setSpeed(SPEED2);
steppery.runSpeed();
  }
 
}


stepperx.setCurrentPosition(0);
steppery.setCurrentPosition(0);
stepperz.setCurrentPosition(0);
  Serial.print('1');



  
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void EAT(Coordinates epoint1,Coordinates epoint2){
  //UNSHIFTED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if(Y1 > -1){ 

  Y1-=1;
}
else if(Y1 <= -1 && a==0){
  Y1=7;
  OUT-=1;
  a+=1;


}
else if( Y1 <= -1 && a==1 && b==0 ){
  Y1=7;
  OUT=9;


   b+=1;
  }
else if( Y1 <= -1 && a==1 && b==1){
  OUT+=1;
  Y1=7;


  }
  epointf={OUT,Y1};

MOVE(epoint1,epointf);
MOVE(epoint2,epoint1);
Serial.print("1");
}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void setup() {
  pinMode(BT,INPUT);
  Serial.begin(9600);
 stepperx.setMaxSpeed(MAX);
 steppery.setMaxSpeed(MAX);
 stepperz.setMaxSpeed(MAX);
servo.attach(11);

if(Serial.available()>0){
pinMode(p1,INPUT);
pinMode(p2,INPUT);
pinMode(p3,INPUT);
ENDSTOP1=digitalRead(p1);
ENDSTOP2=digitalRead(p2);
ENDSTOP3=digitalRead(p3);
INI2();
while(digitalRead(BT)!=1);
Serial.print('2');
}
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void loop(){
if(Serial.available()>0){

  STRN=Serial.readStringUntil('\0');
  dpoint = {int(STRN[0])-48,int(STRN[1])-48};
dpointf={int(STRN[2])-48, int(STRN[3])-48};
if(STRN[4]=="m"){




/*DONT FORGET -5 */
MOVE(dpoint,dpointf);
}
else if(STRN[4]=="e"){


EAT(dpoint,dpointf);
  
}
else if(STRN[4]=="c" && STRN[0]=="1"){
  //UNSHIFTED
  kpoint ={4,7};
kpointf={6,7};
rpoint ={4,7};
rpointf={6,7};
MOVE(kpoint,kpointf);
MOVE(rpoint,rpointf);
Serial.print("1");
}
else if(STRN[4]=="c" && STRN[0]=="0"){
  //UNSHIFTED
  kpoint ={4,7};
kpointf={2,7};
rpoint ={0,7};
rpointf={3,7};
MOVE(kpoint,kpointf);
MOVE(rpoint,rpointf);
Serial.print("1");
}
while(digitalRead(BT)!=1);
Serial.print('2');
}




 }

  
