from random import randint
from ArduinoPy import ArduinoPy

from time import sleep
from demo_opts import get_device

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

white = (255,255,255)
black = (0,0,0)

class pong:
    def __init__(self):
        
        self.device = get_device()
        
        self.Playing = True

        self.panelPlayer = Image.open("/home/evyatar/images/wall2.jpg").convert("RGBA")
        self.wall = Image.open("/home/evyatar/images/wall.jpg").convert("RGBA")

        self.ball = Image.open("/home/evyatar/images/ball.jpg").convert("RGBA")

        self.background = Image.new("RGBA", self.device.size, "white")
      
        self.PlayGame()

    def PlayGame(self):
        self.panelPos = [0,64]

        self.ballPos = [64, 64]
        self.velocity = [randint(1,2),randint(-2,2)]

        self.lost = False

        self.py = ArduinoPy() 
        
        while self.Playing:
            
            pos = self.py.GetGeneralPosition()

            if pos == "F":
                self.panelPos = (self.panelPos[0], self.panelPos[1] - 3)
                sleep(0.005)
            elif pos == "B":
                self.panelPos = (self.panelPos[0], self.panelPos[1] + 3)
                sleep(0.005)
            
            
            self.device.display(self.background.convert(self.device.mode))   
            self.RestFrame()
            self.BallMove()

        self.__init__()    
    
    def RestFrame(self):
        self.background = Image.new("RGBA", self.device.size, "white")

        self.background.paste(self.panelPlayer, self.panelPos)  
        self.background.paste(self.ball, self.ballPos)
        self.background.paste(self.wall, (115,0))

        if self.ballPos[0] < 0:
          self.PaintText("LOST")       
    
    def BallMove(self):
        
        if self.ballPos[0] > 127:
            self.Ballbounce()
        elif self.ballPos == self.panelPos:
            self.Ballbounce()  
        elif self.ballPos[1] < 1:
            self.velocity = (self.velocity[0],-self.velocity[1])
        elif self.ballPos[1] > 127:    
            self.velocity = (self.velocity[0],-self.velocity[1])

        self.ballPos = (self.velocity[0] + self.velocity[0], self.velocity[1])
        self.ballPos = (self.velocity[0], self.velocity[1] + self.velocity[1])

    def Ballbounce(self):
        self.velocity = (-self.velocity[0], self.velocity[1])
        self.velocity = (self.velocity[0], randint(-2,2))

    def PaintText(self,text):
        I1 = ImageDraw.Draw(self.background)
        font = ImageFont.truetype('arial.ttf', 32) 
        I1.text((10, 49), text=text, font=font, fill=black)

        pixels = self.background.load()
        for x in range(self.background.width):
              y1 = 84
              y2 = 40

              pixels[x,y1] = black
              pixels[x,y1 + 1] = black
              pixels[x,y1 + 2] = black
              pixels[x,y1 + 3] = black
 
              pixels[x,y2] = black
              pixels[x,y2 + 1] = black
              pixels[x,y2 + 2] = black
              pixels[x,y2 + 3] = black

              self.device.display(self.background.convert(self.device.mode))                          
        self.StopGame()            

