# Animation Example
# Sean Lu

time = 0   # use time to move objects from one frame to the next

def setup():
    size (800, 800, P3D)
    perspective (60 * PI / 180, 1, 0.1, 1000)  # 60 degree field of view
    
def draw():
    global time
    time += 0.01

    camera (0, 0, 100, 0, 0, 0, 0,  1, 0)  # position the virtual camera

    background (255, 255, 255)  # clear screen and set background to white
    
    # create a directional light source
    ambientLight(50, 50, 50);
    lightSpecular(255, 255, 255)
    directionalLight (100, 100, 100, -0.3, 0.5, -1)
    
    noStroke()
    specular (180, 180, 180)
    shininess (15.0)
    
    pushMatrix()
    rotateY(-time/3)
    
    # TV Screen
    pushMatrix()
    fill(0, 0, 0)
    translate(-4, 0, 3)
    box(25)
    popMatrix()
    
    # TV Frame
    pushMatrix()
    fill(100, 50, 0)
    scale(1.3, 1, 1)
    box(30)
    popMatrix()
    
    # Two settings knobs
    pushMatrix()
    fill(50, 50, 50)
    translate(14, -8, 14.5)
    scale(3, 3, 1)
    cylinder()
    popMatrix()
    
    pushMatrix()
    fill(50, 50, 50)
    translate(14, -0.5, 14.5)
    scale(3, 3, 1)
    cylinder()
    popMatrix()
    
    # Speaker
    fill(120, 120, 120)
    pushMatrix()
    translate(14, 8, 15)
    scale(1.3, 1, 0.2)
    box(5)
    popMatrix()
    
    # Right antenna
    pushMatrix()
    fill(20, 20, 20)
    rotateZ(PI/5)
    rotateX(PI/2)
    translate(-8, 0, 30)
    scale(0.35, 0.35, 12)
    cylinder()
    popMatrix()
    
    # Left antenna
    pushMatrix()
    fill(20, 20, 20)
    rotateZ(PI/-5)
    rotateX(PI/2)
    translate(8, 0, 30)
    scale(0.35, 0.35, 12)
    cylinder()
    popMatrix()
    
    # Antenna mount
    pushMatrix()
    fill(80, 40, 0)
    translate(0, -5, 0)
    sphereDetail(60)
    sphere(15)
    popMatrix()
    
    popMatrix()
    
    # red box
    #fill (255, 0, 0)
    #pushMatrix()
    #translate (-30, 0, 0)
    #rotateX (time)
    #box(20)
    #popMatrix()
    
    # green sphere
    #fill (0, 250, 0)
    #pushMatrix()
    #translate (0, 8 * sin(4 * time), 0)  # move up and down
    #sphereDetail(60)  # this controls how many polygons are used to make a sphere
    #sphere(10)
    #popMatrix()

    # blue cylinder
    #fill (0, 0, 255)
    #pushMatrix()
    #translate (30, 0, 0)
    #rotateX (-time)
    #scale (10, 10, 10)
    #cylinder()
    #popMatrix()

# cylinder with radius = 1, z range in [-1,1]
def cylinder(sides = 64):
    # first endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, -1)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    # sides
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1, y1, -1)
        normal (x2, y2, 0)
        vertex (x2, y2, -1)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2