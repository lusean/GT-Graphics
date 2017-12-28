# Drawing Routines, like OpenGL
# Sean Lu

from matlib import *

vertexList = []
isOrtho = False
isPerspective = False
l = None
r = None
b = None
t = None
n = None
f = None
fovP = None
nearP = None
farP = None

def gtOrtho(left, right, bottom, top, near, far):
    global isOrtho
    global isPerspective
    global l
    global r
    global b
    global t
    global n
    global f
    isOrtho = True
    isPerspective = False
    l = left
    r = right
    b = bottom
    t = top
    n = near
    f = far

def gtPerspective(fov, near, far):
    global isPerspective
    global isOrtho
    global fovP
    global nearP
    global farP
    isPerspective = True
    isOrtho = False
    fovP = fov
    nearP = near
    farP = far

def gtBeginShape():
    # Clear and initialize vertexList
    vertexList[:] = []

def gtEndShape():       
    vertexList[:] = [] 

def gtVertex(x, y, z):
    # 4x1 matrix of xyz values from parameters
    vertex = [[0 for i in range(1)] for j in range(4)]
    vertex[0][0] = x
    vertex[1][0] = y
    vertex[2][0] = z
    vertex[3][0] = 1
    
    # ctm * vertex
    ctm = stack[len(stack) - 1]
    coordX = None
    coordY = None
    coordZ = None
    coordX = ctm[0][0] * vertex[0][0] + ctm[0][1] * vertex[1][0] + ctm[0][2] * vertex[2][0] + ctm[0][3]
    coordY = ctm[1][0] * vertex[0][0] + ctm[1][1] * vertex[1][0] + ctm[1][2] * vertex[2][0] + ctm[1][3]
    coordZ = ctm[2][0] * vertex[0][0] + ctm[2][1] * vertex[1][0] + ctm[2][2] * vertex[2][0] + ctm[2][3]
    vertex[0][0] = coordX
    vertex[1][0] = coordY
    vertex[2][0] = coordZ
    
    # Orthogonal projection
    if isOrtho == True and isPerspective == False:
        vertex[0][0] = width * (vertex[0][0] - l) / (r - l)
        vertex[1][0] = height * (vertex[1][0] - b) / (t - b)
        vertex[1][0] = height - vertex[1][0]
        
    # Perspective projection
    elif isOrtho == False and isPerspective == True:
        # Convert fov to radians and calculate k
        if abs(z) > 0:
            x1 = vertex[0][0] / abs(vertex[2][0])
            y1 = vertex[1][0] / abs(vertex[2][0])
        else:
            x1 = vertex[0][0]
            y1 = vertex[1][0]
        k = tan(radians(fovP) / 2.0)
        x2 = (x1 + k) * width / (2.0 * k)
        y2 = (y1 + k) * height / (2.0 * k)
        vertex[0][0] = x2
        vertex[1][0] = y2
        vertex[1][0] = height - vertex[1][0]
    
    vertexList.append(vertex)
    
    # Draw line with even number of vertices
    if (len(vertexList) % 2 == 0 and len(vertexList) != 0):
        # Get p and q points from vertexList
        p = vertexList[len(vertexList) - 2]
        q = vertexList[len(vertexList) - 1]
        px = p[0][0]
        py = p[1][0]
        qx = q[0][0]
        qy = q[1][0]
        # Draw
        line(px, py, qx, qy)
        #print ("PX = ", px, "PY = ", py \n, "QX = ", qx, "QY = ", qy)
        vertexList[:] = []
        

        
        