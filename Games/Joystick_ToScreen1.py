from time import sleep
from ArduinoPy import ArduinoPy

from demo_opts import get_device
from PIL import Image

white = (255,255,255)
black = (0,0,0)

thickness = 3

def main():
    background = Image.new("RGB", device.size, "white")
    pixels = background.load()
    py = ArduinoPy()

    while True:
        
        posX,posY, BValue = py.GetJoystickPos()
        pixels[posX,posY] = black
        try:


            for i in range(thickness):
                
                pixels[posX - i,posY - i] = black
                pixels[posX - i,posY + i] = black
                pixels[posX + i,posY + i] = black
                pixels[posX + i,posY - i] = black

                pixels[posX,posY - i] = black
                pixels[posX - i,posY] = black
                pixels[posX,posY + i] = black
                pixels[posX + i,posY] = black
        except:
            print("out of bounderys!")
            
        device.display(background.convert(device.mode))


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass