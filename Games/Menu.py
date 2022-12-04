from time import sleep

from ArduinoPy import ArduinoPy
from XO import xo
from Shoot import shoot
from Pong import pong
from Shutdown import shutdown

from demo_opts import get_device

from PIL import Image, ImageDraw, ImageFont

white = (255,255,255)
black = (0,0,0)

class menu:
    
    def __init__(self):
        self.device = get_device()
        self.OfflineGames = [(xo,"XO.jpeg","XO"),(shoot,"thief.jpg","Shoot"),
        (pong,"pongImg.jpg","Pong"),(shutdown,"shut.jpg","OFF")]

        self.logo = Image.open("/home/evyatar/images/xbox.jpg").convert("RGBA")
        self.background = Image.open("/home/evyatar/images/background.jpeg").convert("RGBA")
         
        I1 = ImageDraw.Draw(self.logo)
        font = ImageFont.truetype('arial.ttf', 20)
        I1.text((10, 83), "ORANGE X", font=font, fill = black)        
        self.device.display(self.logo.convert(self.device.mode))          
        sleep(5)
        self.ChoseOffline()
    
    def ChoseOffline(self):
        GamePos = 0
        py = ArduinoPy()      

        while True:

            self.background = Image.open("/home/evyatar/images/background.jpeg").convert("RGBA") 
            game = self.OfflineGames[GamePos]             
            gameImg = Image.open("/home/evyatar/images/" + game[1]).convert("RGBA")
            self.background.paste(gameImg, (32, 32))

            I1 = ImageDraw.Draw(self.background)
            font = ImageFont.truetype('arial.ttf', 20)
            I1.text((50, 100), game[2] , font=font, fill = white)    
            
            if py.GetGeneralPosition() == "B" and GamePos != len(self.OfflineGames) - 1:
                GamePos += 1
                sleep(0.3)
            elif py.GetGeneralPosition() == "F" and GamePos != 0:
                GamePos -= 1
                sleep(0.3)
           
            pressed = py.GetJoystickPos()[2]
            if pressed:
                game[0]()


            self.device.display(self.background.convert(self.device.mode))          
            



            
menu()
            



        


        
