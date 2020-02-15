import sdl2
import sdl2.ext
import posture 
import random

class ball:
    def __init__(self, _id, _center):
        self.id = _id 

        # center pos
        # target (vector)
        # velocity (scalar) 
        sector = random.randint(0,3)
        if (sector == 0):
            self.pos = posture.posture(_center[0], _center[1], _center[2],
                    random.random(),random.random(),0,     
                    random.random())
        elif (sector == 1):
            self.pos = posture.posture(_center[0], _center[1], _center[2],
                    -random.random(),random.random(),0,     
                    random.random()) 
        elif (sector == 2):
            self.pos = posture.posture(_center[0], _center[1], _center[2],
                    random.random(),-random.random(),0,     
                    random.random()) 
        elif (sector == 3):
            self.pos = posture.posture(_center[0], _center[1], _center[2],
                    -random.random(),-random.random(),0,     
                    random.random())

        self.pos.drag = random.random()

        self.weight=250              # weight of ball (g)
        self.width=18                # width of ball  (cm)
        self.height=18               # height of ball (cm)
        self.length=18               # length of ball (cm)

    def draw(self, surface):
        self.pos.heading = self.pos.target
        x = int(self.pos.center_pos[0]-(self.width/2)) 
        y = int(self.pos.center_pos[1]-(self.length/2))
        w = self.width
        l = self.length

        color = sdl2.ext.Color(255, 255, 0)
        sdl2.ext.fill(surface, color, (x, y, w, l)) 

    def __str__(self):
        print(self.pos)
        return "%d %d %d %d" %(self.weight, self.width, self.height, self.length)


        
