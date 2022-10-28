
#include <Wire.h>

int VRx = A1;
int VRy = A0;
int SW = 12;

int SendMode = 0;

void setup()
{
  Wire.begin(8);
  Wire.onRequest(requestEvent);
  //Serial.begin(9600); 

  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(SW, INPUT_PULLUP); 
}

void requestEvent()
{
  if(SendMode == 0)
  {
    int xPosition = analogRead(VRx);
    int mapX = map(xPosition, 0, 1023, 0, 127);
    Wire.write(mapX);

    SendMode++;
  }else if(SendMode == 1)
  {
    int yPosition = analogRead(VRy);
    int mapY = map(yPosition, 0, 1023, 127, 0);
    Wire.write(mapY);

    SendMode++;
  }else if(SendMode == 2)
  {
    int ButtonVal = digitalRead(SW);
    Wire.write(ButtonVal);

    SendMode = 0;
  }
}

void loop()
{
  
}
