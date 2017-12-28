# Animation Example
# Sean Lu
# Couch is replicated using instancing

time = 0   # use time to move objects from one frame to the next

def setup():
    size (800, 800, P3D)
    perspective (60 * PI / 180, 1, 0.1, 1000)  # 60 degree field of view
    frameRate(60)
    
def draw():
    global time
    time += 0.01
    
    # Duration
    # Terminate animation
    if frameCount > 1000:
        exit()

    camera (-70, -50, -40, 0, 0, 0, 0,  1, 0)  # position the virtual camera

    background (255, 255, 255)  # clear screen and set background to white
    
    # Lighting
    ambientLight(50, 50, 50);
    lightSpecular(255, 255, 255)
    directionalLight (120, 100, 100, 0, 1, -2)
    pointLight(50, 50, 50, 0, 5, 1)
    
    noStroke()
    specular (180, 180, 180)
    shininess (15.0)
    
    pushMatrix()
    # Camera Motion
    rotateY(PI + time/8)
    
    # Carpet/Rug
    pushMatrix()
    fill(245, 245, 190)
    translate(-50, 6, 0)
    rotateX(PI/2)
    rect(0, -20, 100, 75)
    popMatrix()
    
    # Person
    pushMatrix()
    # Animations
    if time < 4:
        translate(40 - time * 10, -7.5, 20)
    elif time > 4 and time < 5:
        translate(0, -7.5, 20)
        rotateY((PI/2) * (time - 4))
    elif time > 5 and time < 7.2:
        translate(0, -7.5, -30 + time * 10)
        rotateY(PI/2)
    elif time > 7.2 and time < 8:
        translate(0, -7.5, 42)
        rotateY(PI/2)
    elif time > 8 and time < 9:
        translate(0, -7.5, -38 + time * 10)
        rotateX((PI/-3) * (time - 8))
        rotateY(PI/2) 
    else:
        translate(0, -7.5, 52)
        rotateX(PI/-3)
        rotateY(PI/2)
    rotateY(PI/2)
    person()
    popMatrix()
    
    # Front Couch (Object Instancing)
    pushMatrix()
    translate(2, 0, 0)
    couch()
    popMatrix()
    
    # Side Couch (Object Instancing)
    pushMatrix()
    translate(20, 0, 30)
    rotateY(PI/-2)
    couch()
    popMatrix()
    
    # TV (P2A Object)
    pushMatrix()
    translate(0, -3, 0)
    scale(0.25, 0.25, 0.25)
    TV()
    popMatrix()
    
    # TV Stand
    pushMatrix()
    translate(0, 3, 0)
    scale(4, 1, 3)
    box(5)
    popMatrix()
    
    popMatrix()

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
        
def couch():
    # Back
    pushMatrix()
    fill(245, 245, 220)
    translate(0, 0, 50)
    scale(7, 3, 1)
    box(3)
    popMatrix()
    
    # Seat
    pushMatrix()
    fill(245, 245, 220)
    translate(0, 3, 47)
    scale(7, 1.5, 3)
    box(3)
    popMatrix()
    
    # Arm
    pushMatrix()
    fill(245, 245, 220)
    translate(9.8, 1.5, 47)
    scale(0.5, 1.5, 3)
    box(3)
    popMatrix()
    
    # Arm
    pushMatrix()
    fill(245, 245, 220)
    translate(-9.8, 1.5, 47)
    scale(0.5, 1.5, 3)
    box(3)
    popMatrix()
    
def TV():
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
    
def person():
    # Head
    pushMatrix()
    fill(0, 0, 0)
    sphereDetail(30)
    sphere(2)
    popMatrix()
    
    # Torso
    pushMatrix()
    fill(0, 0, 0)
    rotateX(PI/2)
    scale(0.5, 0.5, 4)
    translate(0, 0, -1)
    cylinder()
    popMatrix()
    
    # Leg
    pushMatrix()
    fill(0, 0, 0)
    rotateX(PI/2)
    rotateY(PI/10)
    scale(0.5, 0.5, 3)
    translate(4.7, 0, -3.5)
    cylinder()
    popMatrix()
    
    # Leg
    pushMatrix()
    fill(0, 0, 0)
    rotateX(PI/2)
    rotateY(PI/-10)
    scale(0.5, 0.5, 3)
    translate(-4.7, 0, -3.5)
    cylinder()
    popMatrix()
    
    # Arm
    pushMatrix()
    fill(0, 0, 0)
    rotateX(PI/2)
    rotateY(PI/-4)
    scale(0.5, 0.5, 2)
    translate(-5, 0, -2.3)
    cylinder()
    popMatrix()
    
    # Arm
    pushMatrix()
    fill(0, 0, 0)
    rotateX(PI/2)
    rotateY(PI/4)
    scale(0.5, 0.5, 2)
    translate(5, 0, -2.3)
    cylinder()
    popMatrix()
    