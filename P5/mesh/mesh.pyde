# Sean Lu
# CS 3451
# Project 5
# Mesh Processing

rotate_flag = True    # automatic rotation of model?
time = 0   # keep track of passing time, for automatic rotation
global vertexList
global cornerList
global colorToggle
global normalToggle
global rand
global oppositeList
vertexList = []
cornerList = []
colorToggle = False
normalToggle = False
rand = 0
oppositeList = {}

# initalize stuff
def setup():
    size (600, 600, OPENGL)
    noStroke()

# draw the current mesh
def draw():    
    global time
    global rand
    
    background(0)    # clear screen to black

    perspective (PI*0.333, 1.0, 0.01, 1000.0)
    camera (0, 0, 5, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    scale (1, -1, 1)    # change to right-handed coordinate system
    
    # create an ambient light source
    ambientLight (102, 102, 102)
  
    # create two directional light sources
    lightSpecular (204, 204, 204)
    directionalLight (102, 102, 102, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    fill (200, 200, 200)            # set polygon color
    ambient (200, 200, 200)
    specular (0, 0, 0)            # no specular highlights
    shininess (1.0)
  
    rotate (time, 1.0, 0.0, 0.0)

    # THIS IS WHERE YOU SHOULD DRAW THE MESH
    randomSeed(rand)
    for i in range(0, len(cornerList) / 3):
        v1 = vertexList[cornerList[i * 3]]
        v2 = vertexList[cornerList[i * 3 + 1]]
        v3 = vertexList[cornerList[i * 3 + 2]]
    
        if colorToggle:
            fill(random(0, 255), random(0, 255), random(0, 255))
    
        beginShape()
        
        if normalToggle:
            n1 = getNormal(v1)
            normal(n1.x, n1.y, n1.z)
        vertex(v1.x, v1.y, v1.z)
        if normalToggle:
            n2 = getNormal(v2)
            normal(n2.x, n2.y, n2.z)
        vertex(v2.x, v2.y, v2.z)
        if normalToggle:
            n3 = getNormal(v3)
            normal(n3.x, n3.y, n3.z)
        vertex(v3.x, v3.y, v3.z)
        
        endShape(CLOSE)        
    
    popMatrix()
    
    # maybe step forward in time (for object rotation)
    if rotate_flag:
        time += 0.02

# process key presses
def keyPressed():
    global rotate_flag
    global normalToggle
    global colorToggle
    #global rand
    if key == ' ':
        rotate_flag = not rotate_flag
    elif key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == '5':
        read_mesh ('torus.ply')
    elif key == 'n':
        normalToggle = not normalToggle
    elif key == 'r':
        colorToggle = True
        rand = random(0, 500)
    elif key == 'w':
        colorToggle = False
    elif key == 'd':
        dual()
    elif key == 'q':
        exit()

# read in a mesh file (THIS NEEDS TO BE MODIFIED !!!)
def read_mesh(filename):
    global cornerList
    global vertexList
    cornerList = []
    vertexList = []

    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
        
    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    # read in the vertices
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        #print "vertex = ", x, y, z
        v = Vertex(x, y, z)
        print(v)
        vertexList.append(v)
    
    # read in the faces
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if nverts != 3:
            print "error: this face is not a triangle"
            exit()
        
        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        #print "face =", index1, index2, index3
        # f = Face(index1, index2, index3)
        # faceList.append(f)
        cornerList.append(index1)
        cornerList.append(index2)
        cornerList.append(index3)
    relations()
        
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.faceList = []
        
    def addFace(self, f):
        self.faceList.append(f)
    
    def plus(self, vert):
        v = Vertex(self.x+vert.x, self.y+vert.y, self.z+vert.z)
        return v

    def minus(self, vert):
        v = Vertex(self.x-vert.x, self.y-vert.y, self.z-vert.z)
        return v
    
    def divide(self, n):
        v = Vertex(self.x/n, self.y/n, self.z/n)
        return v
    
    def vNormalize(self):
        l = sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
        v = Vertex(self.x/l, self.y/l, self.z/l)
        return v
    
    def vCross(self, vert):
        v = Vertex(self.y*vert.z-self.z*vert.y, self.z*vert.x-self.x*vert.z, self.x*vert.y-self.y-vert.x)
        return v
        
class Face:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.centroid = None
        
    def setCentroid(v):
        self.centroid = v
                    
def getNormal(v):
    vert = Vertex(0, 0, 0)
    for x in range(len(v.faceList)):
        i = v.faceList[x]
        v1 = vertexList[cornerList[i * 3]]
        v2 = vertexList[cornerList[i * 3 + 1]]
        v3 = vertexList[cornerList[i * 3 + 2]]
        n = v2.minus(v1).vNormalize().vCross(v3.minus(v1).vNormalize())
        vert = vert.plus(n)
    vert = vert.divide(len(v.faceList)).vNormalize()
    return vert
    
def relations():
    global oppositeList
    global vertexList
    global cornerList
    oppositeList = {}
    for i in range(0, len(cornerList), 3):
        v1 = vertexList[cornerList[i]]
        v2 = vertexList[cornerList[i+1]]
        v3 = vertexList[cornerList[i+2]]
        f = Face(v1, v2, v3)
        v1.addFace(f)
        v2.addFace(f)
        v3.addFace(f)
        
    for i in range(len(cornerList)):
        a = i
        prevA = prevCorner(a)
        nextA = nextCorner(a)
        for j in range(len(cornerList)):
            b = j
            prevB = prevCorner(b)
            nextB = nextCorner(b)            
            if cornerList[prevA] == cornerList[nextB] and cornerList[nextA] == cornerList[prevB]:
                oppositeList[a] = b
                oppositeList[b] = a
                
def getTriangle(c):
    return int(c/3)

def nextCorner(c):
    return 3 * getTriangle(c) + (c+1) % 3

def prevCorner(c):
    return nextCorner(nextCorner(c))

def left(c):
    return oppositeList[nextCorner(c)]

def right(c):
    return oppositeList[prevCorner(c)]

def swing(c):
    return nextCorner(oppositeList[nextCorner(c)])

def getCentroid(a, b, c):
    x = a.x + b.x + c.x
    y = a.y + b.y + c.y
    z = a.z + b.z + c.z
    return Vertex(x/3, y/3, z/3)    

def dual():
    global vertexList
    global cornerList
    newVertexList = []
    newCornerList = []
    
    for i in range(0, len(cornerList), 3):
        v1 = vertexList[cornerList[i]]
        v2 = vertexList[cornerList[i+1]]
        v3 = vertexList[cornerList[i+2]]
        c =  getCentroid(v1, v2, v3)
        newVertexList.append(c)
        
    for i in range(len(vertexList)):
        starting = 0
        for j in range(len(cornerList)):
            if cornerList[j] == i:
                starting = j
                break
        adjCornerList = []
        adjCornerList.append(starting)
        currCorner = swing(starting)
        while currCorner != starting:
            adjCornerList.append(currCorner)
            currCorner = swing(currCorner)
        
        centroid = Vertex(0, 0, 0)
        for j in range(len(adjCornerList)):
            tri = adjCornerList[j] / 3
            currCentroid = newVertexList[tri]
            centroid = centroid.plus(currCentroid)
        centroid = centroid.divide(len(adjCornerList))
        newVertexList.append(centroid)
        
        for j in range(len(adjCornerList)):
            currTri = getTriangle(adjCornerList[j])
            adjTri = getTriangle(adjCornerList[(j+1)%len(adjCornerList)])
            newCornerList.append(currTri)
            newCornerList.append(adjTri)
            newCornerList.append(len(newVertexList)-1)
    
    vertexList = newVertexList
    cornerList = newCornerList
    relations()
             