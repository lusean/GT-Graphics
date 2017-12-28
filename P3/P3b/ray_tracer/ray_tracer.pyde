# Sean Lu
# CS 3451 P3B Shading for Ray Tracing
#
# This is the starter code for the CS 3451 Ray Tracing project.
#
# The most important part of this code is the interpreter, which will
# help you parse the scene description (.cli) files.

shapeList = []
lightList = []
surfaceList = []
bkgd = (0, 0, 0)
vertexList = []

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
    elif key == '0':
        interpreter("i10.cli")

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
            s.surface(surfaceList[len(surfaceList) - 1])
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
            vertexList = []
        elif words[0] == 'vertex':
            triX = float(words[1])
            triY = float(words[2])
            triZ = float(words[3])
            v = PVector(triX, triY, triZ)
            vertexList.append(v)
        elif words[0] == 'end':
            t = Triangle(vertexList[0], vertexList[1], vertexList[2])
            t.surface(surfaceList[len(surfaceList) - 1])
            shapeList.append(t)
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
            closestShape = None
            pt = None
            for index in range(len(shapeList)):
                #Intersect formulas
                s = shapeList[index]
                minT = 10000000
                intersectPt = s.intersects(eyeRay)
                if (intersectPt is not None and
                    (pt is None or originDistance(intersectPt) < originDistance(pt))):
                    closestShape = s
                    pt = intersectPt
            if closestShape is None:
                pix_color = color(bkgd[0], bkgd[1], bkgd[2])
            else:
                r = 0
                g = 0
                b = 0
                calc = calcColor(eyeRay, closestShape, pt, r, g, b, 0)
                pix_color = color(calc[0], calc[1], calc[2])
            set(i, j, pix_color)
    # Reset values for new scene
    shapeList = []
    lightList = []
    surfaceList = []
    bkgd = (0, 0, 0)


# should remain empty for this assignment
def draw():
    pass
    
def calcColor(eyeRay, s, pt, r, g, b, reflectNum):
    n = s.getNormal(pt)
    offset = PVector.mult(n, .0001)
    pt.add(offset)
    if (reflectNum < 5 and s.surf.krefl > 0):
        dir = eyeRay.endPt.normalize()
        reflDir = Ray(pt, (n * (2 * n.dot(dir))).add(dir))
        closestRefl = None
        reflPt = None
        for index in range(len(shapeList)):
            if (shapeList[index] != s):
                intersectRefl = shapeList[index].intersects(reflDir)
                if (intersectRefl is not None and
                        (reflPt is None or originDistance(intersectRefl) < originDistance(reflPt))):
                        closestRefl = shapeList[index]
                        reflPt = intersectRefl
        if closestRefl is not None:
            newColor = calcColor(reflDir, closestRefl, reflPt, r, g, b, reflectNum + 1)
            r += s.surf.krefl * newColor[0]
            g += s.surf.krefl * newColor[1]
            b += s.surf.krefl * newColor[2]
        else:
            r += s.surf.krefl * bkgd[0]
            g += s.surf.krefl * bkgd[1]
            b += s.surf.krefl * bkgd[2]
    
    r += s.surf.car
    g += s.surf.cag
    b += s.surf.cab
    for index in range(len(lightList)):
        light = lightList[index]
        lVector = PVector(light.x, light.y, light.z)
        lRay = Ray(pt, PVector.sub(lVector, pt))
        lightPt = None
        for index2 in range(len(shapeList)):
            intersectLight = shapeList[index2].intersects(lRay)
            if (intersectLight is not None and
                    (lightPt is None or originDistance(intersectLight) < originDistance(pt))):
                    lightPt = intersectLight
        if lightPt is None or originDistance(lightPt) > originDistance(lVector):
            cosine = abs(lRay.endPt.dot(n) / (lRay.endPt.mag() * n.mag()))
            r += cosine * s.surf.cdr * light.r
            g += cosine * s.surf.cdg * light.g
            b += cosine * s.surf.cdb * light.b
            
            #max(0, e . r) ^ p
            phonge = eyeRay.endPt.normalize()
            phongl = lRay.endPt.normalize()
            phongr = PVector.sub((n * (2 * n.dot(phongl))), phongl)
            if phonge.dot(phongr) < 0:
                # (e.r) ^ p
                phong = (phonge.dot(phongr)) ** s.surf.p
                r += phong * s.surf.csr * light.r
                g += phong * s.surf.csg * light.g
                b += phong * s.surf.csb * light.b
    endColor = [r, g, b]
    return endColor
    
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
        
# Use PVector instead
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
class Ray:
    def __init__(self, origin, endPt):
        self.origin = origin
        self.endPt = endPt
    
    def calcPoint(self, t):
        v = PVector(self.origin.x + t * self.endPt.x, self.origin.y +
                   t * self.endPt.y, self.origin.z + t * self.endPt.z)
        return v;
        
class Sphere:
    def __init__(self, r, x, y, z):
        self.r = r
        self.x = x
        self.y = y
        self.z = z
        self.surf = None
    
    def getNormal(self, v):
        center = PVector(self.x, self.y, self.z)
        n = PVector.sub(center, v).normalize()
        return n
        
    # Set surface of sphere
    def surface(self, surf):
        self.surf = surf
        
    def intersects(self, ray):
        # Initialize variables for equations
        x0 = ray.origin.x
        y0 = ray.origin.y
        z0 = ray.origin.z
        x1 = self.x
        y1 = self.y
        z1 = self.z
        r = self.r
        dx = ray.endPt.x
        dy = ray.endPt.y
        dz = ray.endPt.z
            
        # Quadratic formula setup
        a = dx**2 + dy**2 + dz**2
        b = 2 * ((x0 * dx - x1 * dx) + (y0 * dy - y1 * dy) + (z0 * dz - z1 * dz)) 
        c = (x0 - x1)**2 + (y0 - y1)**2 + (z0 - z1)**2 - r**2
        disc = (b**2) - (4 * a * c)
        # Intersects when non-negative discriminant root
        if disc >= 0:     
            # Grab closest root value for t         
            t1 = (-b - sqrt(disc)) / (2 * a)
            t2 = (-b + sqrt(disc)) / (2 * a)
            t = min(t1, t2)
            if t >= 0:
                pt = ray.calcPoint(t)
                return pt
            else:
                return None
        else:
            return None
        
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
        
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
class Triangle:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.surf = None
        
    def surface(self, surf):
        self.surf = surf
        
    def getCenter(self):
        cx = (self.v1.x + self.v2.x + self.v3.x) / 3
        cy = (self.v1.y + self.v2.y + self.v3.y) / 3
        cz = (self.v1.z + self.v2.z + self.v3.z) / 3
        v = PVector(cx, cy, cz)
        return v
    
    def getNormal(self):
        a = PVector.sub(self.v1, self.v2)
        b = PVector.sub(self.v1, self.v3)
        n = a.cross(b)
        return n
    
    def getNormal(self, pt):
        a = PVector.sub(self.v1, self.v2)
        b = PVector.sub(self.v1, self.v3)
        n = a.cross(b)
        return n
            
    def intersects(self, ray):
        o = ray.origin
        r = ray.endPt
        n = self.getNormal(o)
        q = self.getCenter()
        qo = PVector(o.x - q.x, o.y - q.y, o.z - q.z)
        if r.dot(n) == 0:
            return None
        t = -1 * (qo.dot(n) / r.dot(n))
        if t >= 0:
            rt = ray.calcPoint(t)
            if (PVector.sub(self.v2, self.v1).cross(PVector.sub(rt, self.v1)).dot(n) >= 0 and
                PVector.sub(self.v3, self.v2).cross(PVector.sub(rt, self.v2)).dot(n) >= 0 and
                PVector.sub(self.v1, self.v3).cross(PVector.sub(rt, self.v3)).dot(n) >= 0):
                return rt                
            else:
                return None
        else:
            return None
        