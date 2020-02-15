"""2D drawing examples."""
import glm
import draw

class trench:
    def __init__(self, xStart, yStart, color):
        self.color = color
        self.xStart = xStart
        self.yStart = yStart

    def draw(self, surface):
        length =548.64
        width=140.97
        draw.draw_box(surface, glm.vec3(self.xStart,self.yStart,0),length,width,self.color)

