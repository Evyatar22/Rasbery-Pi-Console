from ArduinoPy import ArduinoPy

from time import sleep
from demo_opts import get_device

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

white = (255,255,255)
black = (0,0,0)

class xo:

    def __init__(self):
        self.device = get_device()
        
        self.Playing = True

        self.O = Image.open("/home/evyatar/images/o.jpg").convert("RGB")
        self.X = Image.open("/home/evyatar/images/x.png").convert("RGB")
        self.background = Image.open("/home/evyatar/images/XOBoard.jpg").convert("RGB")

        self.PlayGame()

    def PlayGame(self):
        self.Xplay = True
        preesed = False
        
        self.Owon = False
        self.Xwon = False
        self.tie = False

        self.py = ArduinoPy() 

        self.Olist = []
        self.Xlist = []
      
        while self.Playing:
            
            posX, posY, ButtonPressed = self.py.GetJoystickPos()
            
            if  self.Xplay :
                if ButtonPressed:
                 preesed = True
                self.PastePos(preesed)
            else:
                if ButtonPressed:
                 preesed = True                    
                self.PastePos(preesed)
            
            preesed = False
            self.device.display(self.background.convert(self.device.mode))   
            self.RestFrame(self.Olist, self.Xlist)
        self.__init__()    

    def RestFrame(self, Olist,Xlist):
        self.background = Image.open("/home/evyatar/images/XOBoard.jpg").convert("RGB")

        for pos in Olist:
            self.background.paste(self.O, pos)
        for pos in Xlist:
            self.background.paste(self.X, pos)  

        if self.tie:
          self.PaintText("TIE")                
        elif self.Owon:
          self.PaintText("O WON")                
        elif self.Xwon:
          self.PaintText("X WON")                


    def PaintText(self,text):
        iter = 100
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
   

    
    def PastePos(self, pressed):
        valX,valY = self.py.GetNumberGeneralPosition()
        
        if  self.Xplay:
            pos = (round(valX * 17), round(valY * 17))
            if not self.ChackHasInArr(self.Xlist,pos) and not self.ChackHasInArr(self.Olist,pos):
                self.background.paste(self.X, (round(valX * 17), round(valY * 17)))                  
                if pressed:
                    self.Xlist.append(pos)
                    self.ChackWon()                      
                    self.Xplay = False
                    sleep(0.4)             
        else:  
            pos = (round(valX * 17), round(valY * 17))
            if not self.ChackHasInArr(self.Xlist,pos) and not self.ChackHasInArr(self.Olist,pos):
                self.background.paste(self.O, (round(valX * 17), round(valY * 17)))
                if pressed:
                    self.Olist.append(pos)
                    self.ChackWon()                      
                    self.Xplay = True
                    sleep(0.4)                     
        

    def ChackHasInArr(self, arr, pos):
        for i in arr:
            if i == pos:
                return True
        return False        

    def ChackWon(self):
        
        amountX = [0,0,0]
        amountY = [0,0,0]
        countX1 = 0
        countX2 = 0

        clearArr = []
        if self.Xplay:
            
            for i in self.Xlist:
                
                if i[0] == round(3.4 * 17):
                    x = 2
                elif i[0] == round(5.7 * 17):
                    x = 3
                else:
                    x = 1

                if i[1] == round(3.4 * 17):
                    y = 2
                elif i[1] == round(5.7 * 17):
                    y = 3
                else:
                    y = 1

                clearArr.append((x,y))   
            

            for i in clearArr:
                amountX[i[0] - 1] += 1
                amountY[i[1] - 1] += 1

            for i in clearArr:
                if i[0] == i[1]:
                    countX1 += 1
                    if i == (2,2):
                        countX2 += 1
                elif (i[0] == 3 and i[1] == 1) or (i[0] == 1 and i[1] == 3):
                    countX2 += 1            
            
            if amountX.__contains__(3) or amountY.__contains__(3) or countX1 == 3 or countX2 == 3:
                self.Xwon = True
        else:

            for i in self.Olist:

                if i[0] == round(3.4 * 17):
                    x = 2
                elif i[0] == round(5.7 * 17):
                    x = 3
                else:
                    x = 1

                if i[1] == round(3.4 * 17):
                    y = 2
                elif i[1] == round(5.7 * 17):
                    y = 3
                else:
                    y = 1

                clearArr.append((x,y))  

            
            for i in clearArr:
                amountX[i[0] - 1] += 1
                amountY[i[1] - 1] += 1

            for i in clearArr:
                if i[0] == i[1]:
                    countX1 += 1
                    if i == (2,2):
                        countX2 += 1
                elif (i[0] == 3 and i[1] == 1) or (i[0] == 1 and i[1] == 3):
                    countX2 += 1            
            
            if amountX.__contains__(3) or amountY.__contains__(3) or countX1 == 3 or countX2 == 3:
                self.Owon = True 

        if len(self.Olist) + len(self.Xlist) == 9:
            self.tie = True

        
    def StopGame(self):
        self.Playing = False


game = xo()


        