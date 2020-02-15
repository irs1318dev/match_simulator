import glm
import draw
import math

class posture:
    def __init__(self, _cx, _cy, _cz, _hx, _hy, _hz, _v):# center, heading, velocity
        self.center_pos=glm.vec3(_cx,_cy,_cz)     # (x,y,z) center pos of self (on field)
        self.target=glm.vec3(_hx,_hy,_hz)         # (x,y,z) vector - current target of element 
        self.heading=glm.vec3(0,-1,0)             # (x,y,z) normalized vector - current direction of element 
        self.velocity=_v                          # current velocity of element along the heading
        self.momentum=glm.vec3(0,0,0)             # (x,y,z) vector - current momentum of element 
        self.accelleration=0.0                    # current accelleration of self
        self.drag=0.0                             # current drag of self 
        self.friction=0.0                         # current friction of surface 

    def tick_update(self):

        # calculate new position (from last pos @50ms ago)
        # distance = (1/1000*50)*glm.length()

        # adjust heading to match target over time
        #angle = draw.angleBetween(self.heading, self.target, self.center_pos)

        #print ("Angle now %f"%(angle))
        #if (math.isnan(angle) != True):
        #    self.heading = draw.rotate_vector(self.heading, angle)
        #else:
        #    print ("Skipping angled adjustment (NaN)")

        #print ("Heading now",self.heading)
        #self.heading = self.target
        #self.heading = self.heading * glm.length(self.target)
        #self.heading.x = int(self.heading.x)
        #self.heading.y = int(self.heading.y)

        # calculate the new position based on velocity 
        new_pos = draw.do_translate_point(self.center_pos, (glm.normalize(self.heading) * self.velocity))
        if ((self.center_pos.x > 0) and (self.center_pos.y > 0)):
            self.center_pos.x = new_pos.x
            self.center_pos.y = new_pos.y
            self.center_pos.z = new_pos.z

#        new_vector = glm.cross(self.velocity, self.accelleration)

        # reduce momentum based on friction (2πMgD)?
        # TODO - fix this calculation
        self.velocity = self.velocity - (self.velocity*(self.drag*.1))
       
        

    def set_drag(self, new_drag):
        self.drag = new_drag

    # takes a glm.vec3
    def set_accel(self, new_accel):
        self.accelleration = new_accel 

    def __str__(self):
        return "posture: %dx%dx%d %dx%dx%d %dx%dx%d %d" %(self.center_pos[0], self.center_pos[1], self.center_pos[2], self.heading[0], self.heading[1], self.heading[2], self.target[1], self.target[2], self.velocity)


