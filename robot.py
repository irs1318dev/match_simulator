import sdl2
import sdl2.ext
import glm
import posture
import random
import draw
import ball
import field
from enum import Enum
import time
import math

class state(Enum):
    IDLE = 1
    COLLECT = 2
    AVOID = 3
    DEFEND = 4
    FIRE = 5
    HANG = 6

class robot:
    def __init__(self, num):

        self.id = num
        self.state = state.IDLE

        # x,y,z center pos of robot (on field)
        self.pos = posture.posture(random.randint(0,1500),random.randint(0,800),0,
                                    0,0,0,
                                    0.0)

        self.color = sdl2.ext.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))

        # target for ball delivery
        self.firing_target = glm.vec3(random.randint(0,1500), random.randint(0,800), 0)

        self.collide_ray=[]
        self.collide_ray.append(glm.vec3(0,-1,0))

        self.momentum=0             # current momentum of robot

        self.weight=0               # weight of robot
        self.width=100               # width of robot
        self.height=100             # height of robot
        self.length=100             # length of robot

        #variables handling ball loading
        self.balls_held=3           # number of balls currently held
        self.ball_capacity=5        # total capacity
        self.ground_loading_rate=0  # time to load 1 ball
        self.ground_loading_timer=0 # timer for tracking ball load
        self.top_loading_rate=0     # time to load 1 ball

        # variables handling robot motion
        self.top_speed=10          # top speed of robot (16ft/s)
        self.max_accel=1           # robots top accelleration rate
        self.turning_radius = 2    # robot turn radius

        # variables handling firing
        self.can_fire=1             # can the robot shoot
        self.firing_rate=250        # speed of chamber->fire 
        self.firing_timer=0         # elapsed time to shot 
        self.firing_velocity=5      # nominal velocity of projectile
        self.firing_range=300        # max range of shot
        self.firing_accuracy=.80    # firing accuracy (% success) 
        self.fire_pos=1             # direction robot can fire (front, back, left, right, turret)
        self.turret_velocity=1      # speed of turret (rotational speed)

        self.can_dump=0             # robot can dump to lower port
        self.dump_rate=1            # speed to unload on dump
        self.dump_pos=1             # direction robot can dump (front, back, left, right, turret)

        # variables for color wheel
        self.rotation_speed=1       # rotational speed of controller
        self.rotation_accel=1       # rotational accelleration
        self.rotation_decel=1       # rotational decelleration
        self.color_time=1           # acquisition time for color

        # variables for climbing
        self.extend_rate=1          # speed of extending climber
        self.climb_rate=1           # speed of retracting (climbing)
        self.time_to_balance=1      # time to achieve balance

    def get_mesh(self):
        box_points=[]
        box_points.append(glm.vec3( int(-self.length/2),
                                    int(-self.width/2),
                                    0))
        box_points.append(glm.vec3( int(-self.length/2)+self.length,
                                    int(-self.width/2),
                                    0))
        box_points.append(glm.vec3( int(-self.length/2)+self.length,
                                    int(-self.width/2)+self.width,
                                    0))
        box_points.append(glm.vec3( int(-self.length/2),
                                    int(-self.width/2)+self.width,
                                    0))
        box_points.append(glm.vec3( int(-self.length/2),
                                    int(-self.width/2),
                                    0))
        # draw the triangle (front)
        box_points.append(glm.vec3( 0,
                                    0,
                                    0))
        box_points.append(glm.vec3( int(-self.length/2)+self.length,
                                    int(-self.width/2),
                                    0))
        return (box_points.copy()) 


    def draw(self, surface):
        box_points=self.get_mesh()

        # determine the angle rotation to match target (absolute bearing)
        angle_target = draw.angleBetween(glm.vec3(0,-1,0), self.pos.target)


        # determine the delta between our current heading and the target
        angle_heading = draw.angleBetween(self.pos.heading, self.pos.target)
        angle_heading = angle_heading/self.turning_radius

        # TODO - adjust how much angle rotation happens based on speed to rotate
        self.pos.heading = draw.rotate_vector(self.pos.heading, angle_heading)
        #self.pos.heading.x = self.pos.heading.x*100
        #self.pos.heading.y = self.pos.heading.y*100
        #self.pos.heading.z = self.pos.heading.z*100

        # recalculate the heading after rotation
        angle_heading = draw.angleBetween(glm.vec3(0,-1,0), self.pos.heading)

        draw.draw_mesh(surface, box_points, self.pos.center_pos, angle_heading, self.color)

        draw_ray=[]
        draw_ray.append(glm.vec3(0,-20,0)*self.pos.velocity)
        #draw_ray.append(glm.vec3(0,-10,0))

        draw.draw_rays(surface, draw_ray, self.pos.center_pos, angle_heading, self.color)
        #draw.collide_rays(draw_ray, self.pos.center_pos, angle_heading)


        self.draw_ball(surface, self.firing_target.x, self.firing_target.y, 18, self.color)
        
        yellow= sdl2.ext.Color(255,255,0)
        if (self.balls_held == 1):
            self.draw_ball(surface, self.pos.center_pos.x, self.pos.center_pos.y,18, yellow)
        elif (self.balls_held == 2):
            self.draw_ball(surface, self.pos.center_pos.x-(self.width/4), self.pos.center_pos.y-(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x+(self.width/4), self.pos.center_pos.y+(self.length/4),18,yellow)
        elif (self.balls_held == 3):
            self.draw_ball(surface, self.pos.center_pos.x, self.pos.center_pos.y,18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x-(self.width/4), self.pos.center_pos.y-(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x+(self.width/4), self.pos.center_pos.y+(self.length/4),18,yellow)
        elif (self.balls_held == 4):
            self.draw_ball(surface, self.pos.center_pos.x-(self.width/4), self.pos.center_pos.y-(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x+(self.width/4), self.pos.center_pos.y+(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x+(self.width/4), self.pos.center_pos.y-(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x-(self.width/4), self.pos.center_pos.y+(self.length/4),18,yellow)
        elif (self.balls_held == 5):
            self.draw_ball(surface, self.pos.center_pos.x, self.pos.center_pos.y,18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x-(self.width/4), self.pos.center_pos.y-(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x+(self.width/4), self.pos.center_pos.y+(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x+(self.width/4), self.pos.center_pos.y-(self.length/4),18,yellow)
            self.draw_ball(surface, self.pos.center_pos.x-(self.width/4), self.pos.center_pos.y+(self.length/4),18,yellow)


    def draw_ball(self, surface, xPos, yPos, size, color):
        x = int(xPos-size/2) 
        y = int(yPos-size/2)
        w = size 
        l = size 

        sdl2.ext.fill(surface, color, (x, y, w, l)) 

    def plan_move(self, field):

        if (self.state == state.IDLE):
            if (len(field.power_cells) > 0):
                self.state = state.COLLECT
        elif (self.state == state.COLLECT):
            # pick the target
            if ((self.balls_held < self.ball_capacity) and (len(field.power_cells) > 0)):
                nearest= self.find_nearest_ball(field.power_cells)

                # get the heading (destination - current)
                direction = glm.vec3(nearest.pos.center_pos - self.pos.center_pos); 
                self.pos.target = direction

                #see if we're going to collide with another robot
                draw_ray=[]
                draw_ray.append(glm.vec3(0,-20,0)*self.pos.velocity)

                angle_heading = draw.angleBetween(glm.vec3(0,-1,0), self.pos.heading)
                ray_collisions = draw.collide_rays(field, draw_ray, self.pos.center_pos, angle_heading)     
                # if ray_collisions is not empty, we had a hit
                # depending on where the hit was, we should turn left, right or decrease speed              
                # take a hard right, JIC
                if (len(ray_collisions) > 0):
                    self.pos.heading = draw.rotate_vector(self.pos.heading, 1)
                    print ("Collision")

                col_count = len(ray_collisions)
                col=0
                while (col < col_count):
                    print(ray_collisions[col].x, ray_collisions[col].y, ray_collisions[col].z)
                    col += 1

                # get the distance (TODO: scale accel by distance)
                distance = glm.distance(nearest.pos.center_pos, self.pos.center_pos);  
                if (distance > self.width/2):

                    print ("nearest %d %d %d %d %d %d %d %d" %(nearest.id, nearest.pos.center_pos.x, nearest.pos.center_pos.y, distance, self.pos.target.x, self.pos.target.y, direction.x, direction.y))

                    # TODO: set accel rate based on distance to target
                    self.pos.accelleration += self.max_accel/20
                    if (self.pos.accelleration > self.max_accel):
                        self.pos.accelleration = self.max_accel

                    # adjust the velocity to  velocity += (accelrate/30)
                    self.pos.velocity += self.pos.accelleration 

                    # limit velocity to top speed 
                    if (self.pos.velocity > self.top_speed):
                        self.pos.velocity = self.top_speed
                    if (self.pos.velocity < 0):
                        self.pos.velocity = 0

                    print ("velocity now %d %d"%(self.pos.velocity, self.top_speed))
                else:
                    print ("Caught %d"%(nearest.id))
                    self.pos.velocity = 0
                    self.pos.accelleration = 0;
                    self.balls_held += 1
                    field.remove_ball(nearest.id)
            else:
                self.state = state.FIRE
        elif (self.state == state.FIRE):
            # get the heading (destination - current)
            direction = glm.vec3(self.firing_target - self.pos.center_pos); 

            # convert it to a scale of 1
            #direction = glm.normalize(direction);  
            self.pos.target = direction

                # get the distance (TODO: scale accel by distance)
            distance = glm.distance(self.firing_target, self.pos.center_pos);  

            if (distance > self.firing_range):

                # TODO: set accel rate based on distance to target
                self.pos.accelleration = self.max_accel

                # adjust the velocity to  velocity += (accelrate/30)
                self.pos.velocity += (self.pos.accelleration*(1/20)) 

                # limit velocity to top speed 
                if (self.pos.velocity > self.top_speed):
                    self.pos.velocity = self.top_speed
                if (self.pos.velocity < 0):
                    self.pos.velocity = 0
            else:
                # in firing range
                if (self.firing_timer == 0):
                    self.firing_timer = (time.time()*1000)+self.firing_rate

                if (self.firing_timer <= (time.time()*1000)):
                    self.pos.velocity = 0
                    self.pos.accelleration = 0
                    self.balls_held -= 1
                    self.firing_timer = 0

                    shot_val = random.random();
                    if (shot_val < self.firing_accuracy):
                        # handle scoring
                        # ball goes to queue for re-introduction
                        print("Hit")
                    else:
                        # ball goes back to field
                        # angle of deflection and 1/2 launching speed 
                        print("Miss")

                if (self.balls_held == 0):
                    self.state = state.IDLE


    def find_nearest_ball(self, nodes):
        closest_node = ball.ball(50, glm.vec3(5000,5000,5000))

        nearest = glm.distance(self.pos.center_pos , closest_node.pos.center_pos)
        for n in nodes:
            distance = glm.distance(self.pos.center_pos, n.pos.center_pos)
            if (distance < nearest):
                nearest = distance
                closest_node = n
        return closest_node 

    def __str__(self):
        return "%dx%d %dx%d %3.2f" %(self.center_pos[0], self.center_pos[1], self.center_pos[2], self.heading[0], self.heading[1], self.momentum)


        
