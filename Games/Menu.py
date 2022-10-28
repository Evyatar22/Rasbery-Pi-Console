from time import sleep

from ArduinoPy import ArduinoPy
from XO import xo

from demo_opts import get_device

from PIL import Image, ImageDraw, ImageFont

white = (255,255,255)
black = (0,0,0)

class menu:
    
    def __init__(self):
        self.device = get_device()
        self.OfflineGames = [(xo,"XOBoard.jpg")]

        self.logo = Image.open("/home/evyatar/images/xbox.jpg").convert("RGBA")
        self.background = Image.open("/home/evyatar/images/background.jpg").convert("RGBA")
         
        I1 = ImageDraw.Draw(self.logo)
        font = ImageFont.truetype('arial.ttf', 20)
        I1.text((10, 83), "ORANGE X", font=font, fill = black)        
        self.device.display(self.logo.convert(self.device.mode))          
        
        sleep(10)
    
    def ChoseOffline(self):
        GamePos = 0
        py = ArduinoPy()

        I1 = ImageDraw.Draw(self.background)
        font = ImageFont.truetype('arial.ttf', 10)
        I1.text((10, 83), str(GamePos) , font=font, fill = black)       

        while True:
            if py.GetGeneralPosition() == "B":
                GamePos += 1
                self.background = Image.open("/home/evyatar/images/background.jpg").convert("RGBA")
                game = self.OfflineGames[GamePos]    
                            
                gameImg = Image.open("/home/evyatar/images/" + game[1]).convert("RGBA")
                self.background.paste(gameImg, (self.background.width / 2, self.background.height / 2))
                sleep(0.3)
            elif py.GetGeneralPosition() == "F":
                GamePos -= 1
                self.background = Image.open("/home/evyatar/images/background.jpg").convert("RGBA")
                game = self.OfflineGames[GamePos]    
                            
                gameImg = Image.open("/home/evyatar/images/" + game[1]).convert("RGBA")
                self.background.paste(gameImg, (self.background.width / 2, self.background.height / 2))                
                sleep(0.3)

            self.device.display(self.background.convert(self.device.mode))          
            



            
menu()

            



        


        