from ArduinoPy import ArduinoPy
from demo_opts import get_device

from threading import Thread
import socket
from PIL import ImageFont,Image, ImageDraw
from time import sleep

white = (255,255,255)
black = (0,0,0)
port = 5555

#x = recv, messege = x

class shoot:

    def __init__(self):
        sleep(1)
        self.device = get_device()

        self.Thief = Image.open("/home/evyatar/images/thief2.png").convert("RGB")
        self.Cross = Image.open("/home/evyatar/images/Aim.jpg").convert("RGB")
        self.background = Image.open("/home/evyatar/images/XOBoard.jpg").convert("RGB")

        self.wait = False 
        self.PlayGame()
    
    def PlayGame(self):
        self.Lost = False
        self.Playing = True

        self.py = ArduinoPy()        
        self.ShootPos = []
        self.PasteArray = []

        img = Image.new("RGB", self.device.size, "Black")
        I1 = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 20) 
        I1.text((0, 49), text="Awating client.", font=font, fill=white)
        
        self.device.display(img.convert(self.device.mode))                          
  
        server = socket.socket()
        server.bind(("0.0.0.0",port))
        server.listen(2)
        self.client_socket,addres = server.accept()
        
        Thread(target=self.ChackState).start()
      
        while self.Playing:
            if not self.wait:
                    
                ButtonPressed = self.py.GetJoystickPos()[2]
                valX,valY = self.py.GetNumberGeneralPosition()

                pos = [round(valX * 17), round(valY * 17)]
                self.background.paste(self.Cross, (pos[0], pos[1]))  
                            
                if ButtonPressed:
                    self.ShootPos.append(self.py.GetGeneralPosition())
                    self.PasteArray.append(pos)
                    sleep(0.2) 
 
                            
                self.device.display(self.background.convert(self.device.mode))   
                self.RestFrame()   
        server.close()                      
        self.PlayGame()

    def RestFrame(self):
        self.background = Image.open("/home/evyatar/images/XOBoard.jpg").convert("RGB")
        
        for pos in self.PasteArray:
            self.background.paste(self.Cross, pos)  

    
    def ChackState(self):

        while True:
            try:
                state = self.client_socket.recv(1024).decode()
            except:
                self.StopGame()
                break   
            
            if state == "lost":
                self.wait = True
                self.PaintText("Lost")
                self.client_socket.send("OK".encode())  
                self.wait = False
                break
            elif state == "send":
                self.wait = True
                
                arr = ""
                for pos in range(len(self.ShootPos)):
                    if pos == len(self.ShootPos) - 1:
                      arr += self.ShootPos[pos] 
                    else:
                      arr += self.ShootPos[pos] + " "
                
                self.client_socket.send(arr.encode())


                self.ShootPos.clear()
                self.PasteArray.clear()

                sleep(2)
                self.wait = False
             

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
   

    
    def PastePos(self):
        valX,valY = self.py.GetNumberGeneralPosition()
        
        pos = (round(valX * 17), round(valY * 17))
        self.background.paste(self.Cross, (round(valX * 17), round(valY * 17)))                  
        self.ShootPos.append(pos)
   
    def StopGame(self):
        self.Playing = False


