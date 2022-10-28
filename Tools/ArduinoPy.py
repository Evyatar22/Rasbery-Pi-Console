import RPi.GPIO as GPIO
import os

class ArduinoPy:
  
  #y value first?
  def GetJoystickPos(self):
    
    xy = []
    try:
      import smbus
      I2C_ADDRESS = 0x08
      bus = smbus.SMBus(1)

      bus.write_byte(I2C_ADDRESS,0xFF)

      valueX = bus.read_byte(I2C_ADDRESS)
      xy.append(valueX)
      valueY = bus.read_byte(I2C_ADDRESS)
      xy.append(valueY)

      ButtonValue = bus.read_byte(I2C_ADDRESS)

      if ButtonValue == 0:
        ButtonValue = True
      else:
        ButtonValue = False

      xy.append(ButtonValue)
    except:
      xy = [1,1,False]

    return xy
  
  #trash?
  def GetGeneralPosition(self):
    xPosition,  yPosition, button = self.GetJoystickPos()

    if yPosition == 63 and xPosition == 64:
      return "M"
    elif yPosition > 63 and xPosition > 54 and xPosition < 74:
      return "B"
    elif xPosition < 63 and yPosition > 54 and yPosition < 74:
      return "L" 
    elif xPosition > 63 and yPosition > 54 and yPosition < 74:
      return "R"  
    elif yPosition < 63 and xPosition > 54 and xPosition < 74:
      return "F"
  
  def GetNumberGeneralPosition(self):
    xPosition,  yPosition, button = self.GetJoystickPos()

    if yPosition == 63 and xPosition == 64:
      return 3.4, 3.4
    elif yPosition < 54 and xPosition < 54:
      return 1,1 
    elif yPosition < 54 and xPosition > 74:
      return 5.7,1
    elif yPosition > 74 and xPosition < 54: 
      return 1,5.7
    elif  yPosition > 74 and xPosition > 74: 
      return 5.7,5.7
    elif yPosition > 63 and xPosition > 54 and xPosition < 74:
      return 3.4,5.7
    elif xPosition < 63 and yPosition > 54 and yPosition < 74:
      return 1,3.4 
    elif xPosition > 63 and yPosition > 54 and yPosition < 74:
      return 5.7,3.4  
    elif yPosition < 63 and xPosition > 54 and xPosition < 74:
      return 3.4,1

    return 1,1  