import sdl2
import sdl2.ext
import glm
import math

# Draws robot (box) on the colored surface 
def draw_rect(surface, position, width, height, color):
    # draw rect from upper left hand corner
    x = position[0] 
    y = position[1] 
    w = width 
    h = height 

    # Draw the filled rect with the specified color on the surface.
    # We also could create a set of points to be passed to the function
    # in the form
    #
    # fill(surface, color, ((x1, y1, x2, y2), (x3, y3, x4, y4), ...))
    #                        ^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^
    #                          first rect        second rect
    sdl2.ext.fill(surface, color, (x, y, w, h))

# Draws robot (box) on the colored surface 
def draw_box(surface, position, width, height, color):
    # draw rect from upper left hand corner
    x = int(position[0])
    y = int(position[1])
    w = int(width)
    h = int(height)

    # Draw the filled rect with the specified color on the surface.
    # We also could create a set of points to be passed to the function
    # in the form
    #
    # fill(surface, color, ((x1, y1, x2, y2), (x3, y3, x4, y4), ...))
    #                        ^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^
    #                          first rect        second rect
    sdl2.ext.line(surface, color, (x, y, x+w, y))
    sdl2.ext.line(surface, color, (x, y, x, y+h))
    sdl2.ext.line(surface, color, (x+w, y+h, x+w, y))
    sdl2.ext.line(surface, color, (x+w, y+h, x, y+h))

def gen_model_matrix(angle_x, angle_y, angle_z):
    model = glm.mat4(1.0)

    model = glm.translate(model,glm.vec3(0,0,0)) #position = 0,0,0
#  model = glm.rotate(model,glm.radians(angle_x),glm.vec3(1,0,0))#rotation x = 0.0 degrees
#  model = glm.rotate(model,glm.radians(angle_y),glm.vec3(0,1,0))#rotation y = 0.0 degrees
    model = glm.rotate(model,glm.radians(angle_z),glm.vec3(0,0,1))#rotation z = 0.0 degrees
    model = glm.scale(model,glm.vec3(1,1,1)) #scale = 1,1,1

    #ModelMatrix = glm.translate(ModelMatrix, Translation);
    #ModelMatrix = glm.scale(ModelMatrix, Scale);
    #ModelMatrix = glm.rotate(ModelMatrix, rotAngle, Rotation);

    return model 

def draw_mesh(surface, mesh, center, angle, color):
    # scaling FIRST, and THEN the rotation, and THEN the translation.

    # no scaling :-)
    mesh = rotate_points(mesh, angle) 
    mesh = translate_points(mesh, center)
    draw_poly(surface, mesh, color)

def draw_rays(surface, rays, center, angle, color):
    rays = rotate_points(rays, angle)
    rays = translate_points(rays, center)
    sizeofList = len(rays)
    i=0
    while i < (sizeofList):
        if (((int(center.x) > 0) and (int(center.y) > 0) and (int(rays[i].x) > 0) and (int(rays[i].y) > 0)) and
        ((int(center.x) < 1800) and (int(rays[i].x) < 1800) and (int(center.y) < 900) and (int(rays[i].y) < 900))):
            sdl2.ext.line(surface, color, (int(center.x), int(center.y), int(rays[i].x), int(rays[i].y)))
        i += 1

def get_intersect(A, B, C, D):
    # a1x + b1y = c1
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1 * (A.x) + b1 * (A.y)

    # a2x + b2y = c2
    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2 * (C.x) + b2 * (C.y)

    # determinant
    det = a1 * b2 - a2 * b1

    # parallel line
    if det == 0:
        return (glm.vec3(float('inf'), float('inf'), 0))

    # intersect point(x,y)
    x = ((b2 * c1) - (b1 * c2)) / det
    y = ((a1 * c2) - (a2 * c1)) / det
    
    return (glm.vec3(x, y, 0))


def collide_rays(field, rays, center, angle):
    rays = rotate_points(rays, angle)
    rays = translate_points(rays, center)
    collided_rays=[]

    numBots = len(field.robots)
    j=0
    numRays = len(rays)
    while j < (numBots):

        ro_mesh = field.robots[j].get_mesh()
        ro_angle = angleBetween(glm.vec3(0,-1,0), field.robots[j].pos.heading)
        ro_mesh = rotate_points(ro_mesh, ro_angle) 
        ro_mesh = translate_points(ro_mesh, field.robots[j].pos.center_pos)
        mesh_len = len(ro_mesh)
        r=0
        while r < (mesh_len-1):
            i=0
            while i < (numRays):
                #TODO - ray trace and determine if the line terminates inside the boundaries of a bot
                intersect = get_intersect(center, rays[i], ro_mesh[r], ro_mesh[r+1])
                if (intersect.x == float('inf')):
                    collided_rays.append(rays[i])
                i += 1
            r += 1
        j += 1
    return collided_rays

def draw_poly(surface, points, color):
    # draw rect from upper left hand corner
    sizeofList = len(points) 
    i=0
    while i < (sizeofList-1):
        #print("%f %f %f %f"%(points[i].x, points[i].y, points[i+1].x, points[i+1].y)) 
        if ((int(points[i].x) > 0) and (int(points[i].y) > 0) and (int(points[i+1].x) > 0) and (int(points[i+1].y) > 0) and (int(points[i].x) < 1800) and (int(points[i+1].x) < 1800) and (int(points[i].y) < 900) and (int(points[i].y) < 900)):
            sdl2.ext.line(surface, color, (int(points[i].x), int(points[i].y), int(points[i+1].x), int(points[i+1].y))) 
        i += 1

# Draws robot (box) on the colored surface 
def draw_robot(surface, position, width, height):
    # Create a set of four random points for the edges of the rectangle.
    x = position[0] 
    y = position[1] 
    w = width 
    h = height 

    # Create a random color.
    color = sdl2.ext.Color(randint(0, 255),
                randint(0, 255),
                randint(0, 255))

    # Draw the filled rect with the specified color on the surface.
    # We also could create a set of points to be passed to the function
    # in the form
    #
    # fill(surface, color, ((x1, y1, x2, y2), (x3, y3, x4, y4), ...))
    #                        ^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^
    #                          first rect        second rect
    sdl2.ext.fill(surface, color, (x, y, w, h))

def draw_ball(surface, position, width, height):
    x = int(position[0]-width/2) 
    y = int(position[1]-height/2)
    w = width
    h = height

    color = sdl2.ext.Color(255, 255, 0)
    if ((x > 0) and (y > 0) and (x < 1800) and (y < 900)):
        sdl2.ext.fill(surface, color, (x, y, w, h))

def draw_generator():
    return 0 

def draw_trench(surface, _xStartPos, _yStartPos, color):
    length =548.64
    width=140.97
    draw_box(surface, glm.vec3(_xStartPos,_yStartPos,0),length,width,color)

def rotate_vector(vector, angle):
    # takes a vector and returns a normalized vector adjusted by angle
    # angle delivered in degrees
    # simple 2d rotation about the Z axis following sum angle rule
    x2=((vector.x*glm.cos(angle)) - (vector.y*glm.sin(angle)))
    y2=((vector.x*glm.sin(angle)) + (vector.y*glm.cos(angle)))

    # don't hold this to an int
    vector.x = x2
    vector.y = y2

    vector = glm.normalize(vector)

    return vector 

def rotate_points(points_list, angle):
    # passed in mesh is a list of vec3 x,y,z positions
    # rotation happens around the 0,0,0 position
    sizeofList = len(points_list) 
    i=0
    # for every vec3 in mesh 
    while i < (sizeofList):
        # simple 2d rotation about the Z axis following sum angle rule
        x2=((points_list[i].x*glm.cos(angle)) - (points_list[i].y*glm.sin(angle)))
        y2=((points_list[i].x*glm.sin(angle)) + (points_list[i].y*glm.cos(angle)))
        if ((math.isnan(x2) == False) and (math.isnan(y2) == False)):
            points_list[i].x = int(x2)
            points_list[i].y = int(y2)
        i += 1
    return points_list
    
def translate_points(points, center_pos):
    #translate point based on the center pos
    # (move 0,0,0 mesh to center pos)
    sizeofList = len(points) 
    i=0
    while i < (sizeofList):
        points[i].x += center_pos.x 
        points[i].y += center_pos.y
        i += 1
    return points

def do_translate_point(point, vector):
    matrix = glm.mat4(glm.translate(glm.mat4(),point))
    transform = glm.vec4(vector.x, vector.y, vector.z, 1.0)
    return glm.vec4(matrix * transform)

def angleBetween(a, b):
    dot = a.x*b.x + a.y*b.y  # dot product
    det = a.x*b.y - a.y*b.x  # determinant
    angle = math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    return angle

