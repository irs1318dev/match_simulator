import glm
import draw
import math
import copy

# This class handles the orientation, movement and various associated tasks for a given object.

# 
# lots of stuff here shamelessly stolen from 
# https://github.com/SebLague/Boids under the MIT license
# Portions Copyright (c) 2019 Sebastian Lague
# 
# Check out his sweet video:
# https://www.youtube.com/watch?v=bqtqltqcQhw&fbclid=IwAR3MYG37B7dI3EV4YiNySQVSvtj-MP_0xcgWdh7-T18aUoAEg2BNohNWzk0 
#
class posture:
    def __init__(self, _cx, _cy, _cz, _hx, _hy, _hz, _v):# center, heading, velocity
        self.center_pos=glm.vec3(_cx,_cy,_cz)     # (x,y,z) center pos of self (on field)
        self.target=glm.vec3(_hx,_hy,_hz)         # (x,y,z) vector - current target of element 
        self.heading=glm.vec3(0,-1,0)             # (x,y,z) normalized vector - current direction of element (forward)

        self.velocity=_v                          # current velocity of element along the heading
        self.velocity2=glm.vec3(0,0,0)              # (x,y,z) vector - velocity2
        self.momentum=glm.vec3(0,0,0)             # (x,y,z) vector - current momentum of element 
        self.accel2=glm.vec3(0,0,0)                 # (x,y,z) vector - accelleration (2)
        self.avgAvoidanceHeading=glm.vec3(0,0,0)  # (x,y,z) vector - avg avoidance heading 
        self.accelleration=0.0                    # current accelleration of self
        self.drag=0.0                             # current drag of self 
        self.friction=0.0                         # current friction of surface 

        self.minSpeed=0.0                       # minimum speed
        self.maxSpeed=5.0                       # maximum speed
        self.perceptionRadius = 2.5             # radius for perception
        self.avoidanceRadius = 1                # radius for avoidance
        self.maxSteerForce=3.0                  # maximum steerage force

        self.alignWeight=1                      # how much to weigh aligning with the flock
        self.cohesionWeight=1                   # how much to weigh cohesion with the flock
        self.separateWeight=1                   # how much to weigh separation from the flock
        self.targetWeight=1                     # how much to weigh the target destination

        self.boundsRadius = 0.27                # radius of the boundary
        self.avoidCollisionsWeight = 10         # how much to weight avoiding collisions
        self.collisionAvoidDst = 5              # the distance to use when avoiding
        self.collide_rays=self.calc_collide_rays(100, 100)


    def tick_update(self):
        acceleration = glm.vec3(0,0,0)

        if (self.target != glm.vec3(0,0,0)):
            offsetToTarget = glm.vec3(self.target - self.center_pos) 
            accelleration = self.steer_towards(offsetToTarget) * self.targetWeight

# no flocking behavior here
#       if (numPerceivedFlockmates != 0) {
#            centreOfFlockmates /= numPerceivedFlockmates;
#
#            Vector3 offsetToFlockmatesCentre = (centreOfFlockmates - position);
#
#            var alignmentForce = SteerTowards (avgFlockHeading) * settings.alignWeight;
#            var cohesionForce = SteerTowards (offsetToFlockmatesCentre) * settings.cohesionWeight;
#            var seperationForce = SteerTowards (avgAvoidanceHeading) * settings.seperateWeight;
#
#            acceleration += alignmentForce;
#            acceleration += cohesionForce;
#            acceleration += seperationForce;
#        }
 
        if (self.is_heading_for_collision()):
            collisionAvoidDir = glm.vec3(obstacle_rays());
            collisionAvoidForce = glm.vec3(steer_towards(collisionAvoidDir) * self.avoidCollisionWeight)
            acceleration += collisionAvoidForce;

        self.velocity2 += acceleration * 50/1000
        speed = glm.length(self.velocity2) #velocity.magnitude; (TODO: should be magnitude, confirm)
        direction = glm.vec3(self.velocity2 / speed)
        speed = glm.clamp(speed, self.minSpeed, self.maxSpeed);
        self.velocity2 = direction * speed;

#        cachedTransform.position += velocity * 50/1000;
#        cachedTransform.forward = direction;
#        position = cachedTransform.position;

        self.heading = direction;


        # calculate the new position based on velocity 
        new_pos = draw.do_translate_point(self.center_pos, (glm.normalize(self.heading) * self.velocity))
        if ((math.isnan(new_pos.x) == False) and (math.isnan(new_pos.y) == False) and (math.isnan(new_pos.z)== False)):
            if ((self.center_pos.x > 0) and (self.center_pos.y > 0)):
                self.center_pos.x = int(new_pos.x)
                self.center_pos.y = int(new_pos.y)
                self.center_pos.z = int(new_pos.z)

#        new_vector = glm.cross(self.velocity, self.accelleration)

        # reduce momentum based on friction (2πMgD)?
        # TODO - fix this calculation
#        self.velocity = self.velocity - (self.velocity*(self.drag*.1))
       
        

    def set_drag(self, new_drag):
        self.drag = new_drag

    # takes a glm.vec3
    def set_accel(self, new_accel):
        self.accelleration = new_accel 

    def __str__(self):
        return "posture: %dx%dx%d %dx%dx%d %dx%dx%d %d" %(self.center_pos[0], self.center_pos[1], self.center_pos[2], self.heading[0], self.heading[1], self.heading[2], self.target[1], self.target[2], self.velocity)

    def calc_collide_rays(self, numViewDirections, length):
        directions=[]

        goldenRatio = (1 + glm.sqrt(5)) / 2;
        angleIncrement = glm.pi() * 2 * goldenRatio;

        i=0 
        while i < (numViewDirections):
            t =  i / numViewDirections;
            inclination = glm.acos(1 - 2 * t); 
            azimuth = angleIncrement * i;
            x = glm.sin(inclination) * glm.cos(azimuth);
            y = glm.sin (inclination) * glm.sin(azimuth);
            z = glm.cos (inclination); 
            directions.append(glm.vec3(x, y, z)*length)
            i+=1

        return directions 

    def get_collide_rays(self):
        local_rays = copy.deepcopy(self.collide_rays)
        return (local_rays)


    def steer_towards(self, vector):
        v = glm.vec3(glm.normalize(vector) * self.maxSpeed - self.velocity2)
        return glm.clamp(v, 0, self.maxSteerForce);

    def is_heading_for_collision(self):
       # RaycastHit hit;
       # if (Physics.SphereCast (position, settings.boundsRadius, forward, out hit, settings.collisionAvoidDst, settings.obstacleMask)) {
       #     return true;
       # } else { }
        return False     

    def obstacle_rays(self):
        rayDirections = self.get_collide_rays();
        length = rayDirections.length()
        i=0
        while i < (length):
        #    Vector3 dir = cachedTransform.TransformDirection (rayDirections[i]);
            #Ray ray = new Ray (position, dir);
            #if (!Physics.SphereCast (ray, settings.boundsRadius, settings.collisionAvoidDst, settings.obstacleMask)) {
            #    return dir;
            #}
            i += 1		
        

        return self.heading;





