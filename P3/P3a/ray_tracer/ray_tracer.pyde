# Sean Lu
# CS 3451 P3A Ray Tracing Spheres
#
# This is the starter code for the CS 3451 Ray Tracing project.
#
# The most important part of this code is the interpreter, which will
# help you parse the scene description (.cli) files.

shapeList = []
intersectList = []
lightList = []
surfaceList = []
bkgd = (0, 0, 0)

def setup():
    size(500, 500) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)

# read and interpret the appropriate scene description .cli file based on key press
def keyPressed():
    if key == '1':
        interpreter("i1.cli")
    elif key == '2':
        interpreter("i2.cli")
    elif key == '3':
        interpreter("i3.cli")
    elif key == '4':
        interpreter("i4.cli")
    elif key == '5':
        interpreter("i5.cli")
    elif key == '6':
        interpreter("i6.cli")
    elif key == '7':
        interpreter("i7.cli")
    elif key == '8':
        interpreter("i8.cli")
    elif key == '9':
        interpreter("i9.cli")

def interpreter(fname):
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
    # parse each line in the file in turn
    for line in lines:
        words = line.split()  # split the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            radius = float(words[1])
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            # call your sphere creation routine here
            # for example: create_sphere(radius,x,y,z)
            s = Sphere(radius, x, y, z)
            shapeList.append(s)
        elif words[0] == 'fov':
            global fov
            fov = float(words[1])
        elif words[0] == 'background':
            global bkgd
            bkgdR = float(words[1])
            bkgdG = float(words[2])
            bkgdB = float(words[3])
            bkgd = (bkgdR, bkgdG, bkgdB)
        elif words[0] == 'light':
            lightX = float(words[1])
            lightY = float(words[2])
            lightZ = float(words[3])
            lightR = float(words[4])
            lightG = float(words[5])
            lightB = float(words[6])
            l = Light(lightX, lightY, lightZ, lightR, lightG, lightB)
            lightList.append(l)
        elif words[0] == 'surface':
            cdr = float(words[1])
            cdg = float(words[2])
            cdb = float(words[3])
            car = float(words[4])
            cag = float(words[5])
            cab = float(words[6])
            csr = float(words[7])
            csg = float(words[8])
            csb = float(words[9])
            p = float(words[10])
            krefl = float(words[11])
            s = Surface(cdr, cdg, cdb, car, cag, cab, csr, csg, csb, p, krefl)
            surfaceList.append(s)
        elif words[0] == 'begin':
            pass #part b
        elif words[0] == 'vertex':
            pass #part b
        elif words[0] == 'end':
            pass #part b
        elif words[0] == 'write':
            render_scene()    # render the scene
            save(words[1])  # write the image to a file
            pass

# render the ray tracing scene
def render_scene():
    global shapeList
    global surfaceList
    global lightList
    global bkgd
    global intersectList

    for index in range(len(shapeList)):
        shapeList[index].surface(surfaceList[index])
    k = tan(radians(fov/2.0))
    for j in range(height):
        for i in range(width):
            # create an eye ray for pixel (i,j) and cast it into the scene
            origin = PVector(0, 0, 0)
            # x' = i
            # y' = height - j
            # x'' = x' * 2k/w
            # y'' = y' * 2k/h
            v = PVector((i - (width/2))*((2*k)/width), ((height-j)-(height/2))*((2*k)/height), -1)
            # Direction = (x'', y'', z'') - origin
            dir = v - origin
            eyeRay = Ray(origin, dir.normalize())
            # Calculate intersections
            intersectList = []
            for index in range(len(shapeList)):
                #Intersect formulas
                s = shapeList[index]
                # Initialize variables for equations
                x0 = eyeRay.origin.x
                y0 = eyeRay.origin.y
                z0 = eyeRay.origin.z
                x1 = s.x
                y1 = s.y
                z1 = s.z
                r = s.r
                dx = eyeRay.endPt.x
                dy = eyeRay.endPt.y
                dz = eyeRay.endPt.z
            
                # Quadratic formula setup
                a = dx**2 + dy**2 + dz**2
                b = 2 * ((x0 * dx - x1 * dx) + (y0 * dy - y1 * dy) + (z0 * dz - z1 * dz)) 
                c = (x0 - x1)**2 + (y0 - y1)**2 + (z0 - z1)**2 - r**2
                disc = (b**2) - (4 * a * c)
                inter = None
                # Intersects when non-negative discriminant root
                if disc >= 0:     
                    # Grab closest root value for t         
                    t1 = (-b - sqrt(disc)) / (2 * a)
                    t2 = (-b + sqrt(disc)) / (2 * a)
                    t = min(t1, t2)
                    inter = Intersected(eyeRay, s, t, x0, y0, z0, dx, dy, dz)
                    # Add to intersection list
                    intersectList.append(inter)
            minT = sys.maxint
            for index in range(len(intersectList)):
                if (intersectList[index].t >= 0 and intersectList[index].t < minT):
                    minT = intersectList[index].t
                    c = intersectList[index]
            # Shading equation
            if len(intersectList) != 0:
                # R(t) = o + tD
                rt = PVector(c.x0 + c.t * c.dx, c.y0 + c.t * c.dy, c.z0 + c.t * c.dz)
                # Origin point
                o = PVector(c.obj.x, c.obj.y, c.obj.z)
                # Normal vector
                n = (rt - o).normalize()
                r = 0
                g = 0
                b = 0
                for index in range(len(lightList)):
                    # Light coord
                    lightCoord = PVector(lightList[index].x, lightList[index].y, lightList[index].z)
                    # Light vector
                    l = (lightCoord - rt).normalize()
                    # Cl(max(0, N * L)
                    # Total addition of all lights
                    r += lightList[index].r * max(0, n.dot(l))
                    g += lightList[index].g * max(0, n.dot(l))
                    b += lightList[index].b * max(0, n.dot(l))
                # Diffuse coefficient
                r = r * c.obj.surf.cdr
                g = g * c.obj.surf.cdg
                b = b * c.obj.surf.cdb
                pix_color = color(r, g, b)                
            # Normal coloring with no intersect  
            else:
                pix_color = color(bkgd[0], bkgd[1], bkgd[2])
            set(i, j, pix_color)
    # Reset values for new scene
    shapeList = []
    intersectList = []
    lightList = []
    surfaceList = []
    bkgd = (0, 0, 0)


# should remain empty for this assignment
def draw():
    pass
    
def originDistance(v):
    return sqrt(v.x * v.x + v.y * v.y + v.z * v.z)

class Light:
    def __init__(self, x, y, z, r, g, b):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        
class Surface:
    def __init__(self, cdr, cdg, cdb, car, cag, cab, csr, csg, csb, p, krefl):
        self.cdr = cdr
        self.cdg = cdg
        self.cdb = cdb
        self.car = car
        self.cag = cag
        self.cab = cab
        self.csr = csr
        self.csg = csg
        self.csb = csb
        self.p = p
        self.krefl = krefl
        
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
class Ray:
    def __init__(self, origin, endPt):
        self.origin = origin
        self.endPt = endPt
        
class Sphere:
    def __init__(self, r, x, y, z):
        self.r = r
        self.x = x
        self.y = y
        self.z = z
        self.surf = None
        
    # Set surface of sphere
    def surface(self, surf):
        self.surf = surf
        
class Intersected:
    def __init__(self, ray, obj, t, x0, y0, z0, dx, dy, dz):
        self.ray = ray
        self.obj = obj
        self.t = t
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.dx = dx
        self.dy = dy
        self.dz = dz