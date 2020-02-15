import glm
import sdl2
import sdl2.ext
import draw

class generator:
    def __init__(self, _xStartPos, _yStartPos):
        self.xPos = _xStartPos
        self.yPos = _yStartPos
        self.xPos1 =0
        self.yPos1 =0
        self.xPos2 =0
        self.yPos2 =0
        self.xPos3 =0
        self.yPos3 =0
        self.width=459.10
        self.length=459.10
    
    def draw(self, surface):
        position= glm.vec3(self.xPos, self.yPos, 0)
        white = sdl2.ext.Color(255, 255, 255);
        draw.draw_box(surface, position, self.width, self.length, white)

