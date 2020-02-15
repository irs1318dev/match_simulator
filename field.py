import sdl2
import sdl2.ext
import glm
import random
from random_word import RandomWords
import ball
import view
import draw
import trench
import generator
import robot

class field:
    def __init__(self, _startX, _startY):

        self.xFieldStart = _startX
        self.yFieldStart = _startY
        self.xFieldSize=1598
        self.yFieldSize=821
        self.xsize=self.xFieldSize
        self.ysize=self.yFieldSize

        self.power_cells=[]
        self.power_cells_location =[]
        self.power_cells_location.append(glm.vec3((self.xFieldStart+(self.xFieldSize/2)), (self.yFieldStart+70.48), 0))
        self.power_cells_location.append(glm.vec3((self.xFieldStart+(self.xFieldSize/2))-91.44, (self.yFieldStart+70.48), 0))
        self.power_cells_location.append(glm.vec3((self.xFieldStart+(self.xFieldSize/2))-182.88, (self.yFieldStart+70.48), 0))
        self.power_cells_location.append(glm.vec3((self.xFieldStart+(self.xFieldSize/2)), (self.yFieldStart+self.yFieldSize-70.48), 0))
        self.power_cells_location.append(glm.vec3((self.xFieldStart+(self.xFieldSize/2))+91.44, (self.yFieldStart+self.yFieldSize-70.48), 0))
        self.power_cells_location.append(glm.vec3((self.xFieldStart+(self.xFieldSize/2))+182.88, (self.yFieldStart+self.yFieldSize-70.48), 0))


        self.num_power_cells = 20
        for i in range(self.num_power_cells):
            if (i < len(self.power_cells_location)):
                self.power_cells.append(ball.ball(i, self.power_cells_location[i]))
            else:
                self.power_cells.append(ball.ball(i, glm.vec3(int(random.randrange(0,1500)),int(random.randrange(0,900)),0)))

        self.num_robots = 6
        self.robots=[]
        for j in range(self.num_robots):
            self.robots.append(robot.robot(j))

        red = sdl2.ext.Color(255,0,0);
        blue = sdl2.ext.Color(0,0,255);
        self.red_trench = trench.trench(self.xFieldStart+524.68, self.yFieldStart,red)
        self.blue_trench = trench.trench(self.xFieldStart+524.68, self.yFieldStart+self.yFieldSize-130.97,blue)
        self.generator = generator.generator(self.xFieldStart+((self.xFieldStart+self.xFieldSize)/2)-129.69, self.yFieldStart+self.yFieldSize-130.97-459.10)

    def add_ball(self, _x, _y):
        self.num_power_cells += 1 
        self.power_cells.append(ball.ball(self.num_power_cells, glm.vec3(_x,_y,0)))

    def remove_ball(self, _id):
        for i in self.power_cells:
            if( _id == i.id):
                self.power_cells.remove(i)
                return  0;
            
    def reset(self):
        return 0

    def draw(self, surface):
        xInitiationOffset=305

        white = sdl2.ext.Color(255, 255, 255);
        grey = sdl2.ext.Color(50, 50, 50);
        ltred = sdl2.ext.Color(50, 0, 0); 
        ltblue = sdl2.ext.Color(0, 0, 50);
        red = sdl2.ext.Color(255,0,0);
        blue = sdl2.ext.Color(0,0,255);
        green = sdl2.ext.Color(0,255,0);

        # initiation lines
        sdl2.ext.line(surface, white, (self.xFieldStart+xInitiationOffset, self.yFieldStart, self.xFieldStart+xInitiationOffset, self.yFieldStart+self.yFieldSize))
        sdl2.ext.line(surface, white, (self.xFieldSize+self.xFieldStart-(xInitiationOffset), self.yFieldStart, self.xFieldSize+self.xFieldStart-(xInitiationOffset), self.yFieldStart+self.yFieldSize))

        # player lines
        sdl2.ext.line(surface, green, (int(self.xFieldStart-71.12), self.yFieldStart, int(self.xFieldStart-71.12), self.yFieldStart+self.yFieldSize))
        sdl2.ext.line(surface, green, (int(self.xFieldStart+self.xFieldSize+71.12), self.yFieldStart, int(self.xFieldStart+self.xFieldSize+71.12), self.yFieldStart+self.yFieldSize))

        #draw center lines
        sdl2.ext.line(surface, grey, (self.xFieldStart, self.yFieldStart+int(self.ysize/2), self.xFieldStart+self.xsize, self.yFieldStart+int(self.ysize/2)))
        sdl2.ext.line(surface, grey, (self.xFieldStart+int(self.xsize/2), self.yFieldStart, self.xFieldStart+int(self.xsize/2),self.yFieldStart+self.ysize))

        # center lines of loading/delivery
        sdl2.ext.line(surface, grey, (self.xFieldStart, self.yFieldStart+int(240.43), self.xFieldStart+self.xsize,self.yFieldStart+int(240.43)))
        sdl2.ext.line(surface, grey, (self.xFieldStart, self.yFieldStart+int(self.ysize-240.43), self.xFieldStart+self.xsize,self.yFieldStart+int(self.ysize-240.43)))

        # trench
        self.red_trench.draw(surface) 
        self.blue_trench.draw(surface) 
        #draw.draw_trench(surface, self.xFieldStart+524.68, self.yFieldStart,red)
        #draw.draw_trench(surface, self.xFieldStart+524.68, self.yFieldStart+self.yFieldSize-130.97,blue)

        self.generator.draw(surface)

     #   self.draw_box(surface, glm.vec3(self.xFieldStart+xInitiationOffset+220.04,self.yFieldStart,0),458.64,140.97,red)
     #   self.draw_box(surface, glm.vec3(self.xFieldStart+xInitiationOffset+220.04,self.yFieldStart+self.yFieldSize-130.97,0),458.64,140.97,blue)


    def __str__(self):
        return "Name: %s %d %d (%.2f %.2f %.2f)" %(self.name, self.team_id, self.league, self.shoot_skill, self.defense_skill, self.climb_skill)


