# Matrix Stack Library -- Use your code from Project 1A
# Sean Lu

stack = []

def gtInitialize():
    stack[:] = []
    matrix = [[0 for x in range(4)] for y in range(4)]
    matrix[0][0] = 1.0
    matrix[1][1] = 1.0
    matrix[2][2] = 1.0
    matrix[3][3] = 1.0
    stack.append(matrix)    

def gtPushMatrix():
    push_matrix = stack[-1]
    stack.append(push_matrix)

def gtPopMatrix():
    if len(stack) == 1:
        print "Error: Only 1 matrix on stack"
    else:
        stack.pop()

def gtTranslate(x, y, z):
    # Make transformation matrix
    trans_matrix = [[0 for i in range(4)] for j in range(4)]
    trans_matrix[0][3] = x
    trans_matrix[1][3] = y
    trans_matrix[2][3] = z
    trans_matrix[0][0] = 1.0
    trans_matrix[1][1] = 1.0
    trans_matrix[2][2] = 1.0
    trans_matrix[3][3] = 1.0
    # Get old ctm
    old_ctm = stack[len(stack) - 1]
    # Deep copy old to new ctm
    new_ctm = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            new_ctm[i][j] = old_ctm[i][j]    
    for i in range(3):
        new_ctm[i][3] = old_ctm[i][i] * trans_matrix[i][3]
    #stack.append(new_ctm)
    stack[len(stack) - 1] = new_ctm

def gtScale(x, y, z):
    # Make scale matrix
    scale_matrix = [[0 for i in range(4)] for j in range(4)]
    scale_matrix[0][0] = x
    scale_matrix[1][1] = y
    scale_matrix[2][2] = z
    scale_matrix[3][3] = 1.0
    # Get old ctm
    old_ctm = stack[len(stack) - 1]
    # Deep copy old to new ctm
    new_ctm = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            new_ctm[i][j] = old_ctm[i][j]
    for i in range(3):
        new_ctm[i][i] = old_ctm[i][i] * scale_matrix[i][i]
    #stack.append(new_ctm)
    stack[len(stack) - 1] = new_ctm

def gtRotateX(theta):
    # Convert degrees to radians
    rad = radians(theta)
    # Make x rotation matrix
    rot_matrix = [[0 for i in range(4)] for j in range(4)]
    rot_matrix[0][0] = 1.0
    rot_matrix[3][3] = 1.0
    rot_matrix[1][1] = cos(rad)
    rot_matrix[1][2] = -1.0 * sin(rad)
    rot_matrix[2][1] = sin(rad)
    rot_matrix[2][2] = cos(rad)
    # Get old ctm
    old_ctm = stack[len(stack) - 1]
    # Deep copy old to new ctm
    new_ctm = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            new_ctm[i][j] = old_ctm[i][j]
    new_ctm[1][1] = rot_matrix[1][1] * old_ctm[1][1] + rot_matrix[1][2] * old_ctm[2][1]
    new_ctm[2][1] = rot_matrix[2][1] * old_ctm[1][1] + rot_matrix[2][2] * old_ctm[2][1]
    new_ctm[1][2] = rot_matrix[1][1] * old_ctm[1][2] + rot_matrix[1][2] * old_ctm[2][2]
    new_ctm[2][2] = rot_matrix[2][1] * old_ctm[1][2] + rot_matrix[2][2] * old_ctm[2][2]
    #stack.append(new_ctm)
    stack[len(stack) - 1] = new_ctm

def gtRotateY(theta):
    # Convert degrees to radians
    rad = radians(theta)
    # Make y rotation matrix
    rot_matrix = [[0 for i in range(4)] for j in range(4)]
    rot_matrix[0][0] = cos(rad)
    rot_matrix[0][2] = sin(rad)
    rot_matrix[1][1] = 1.0
    rot_matrix[2][0] = -1.0 * sin(rad)
    rot_matrix[2][2] = cos(rad)
    rot_matrix[3][3] = 1.0
    # Get old ctm
    old_ctm = stack[len(stack) - 1]
    # Deep copy old to new ctm
    new_ctm = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            new_ctm[i][j] = old_ctm[i][j]
    new_ctm[0][0] = rot_matrix[0][0] * old_ctm[0][0] + rot_matrix[0][2] * old_ctm[2][0]
    new_ctm[0][2] = rot_matrix[0][0] * old_ctm[0][2] + rot_matrix[0][2] * old_ctm[2][2]
    new_ctm[2][0] = rot_matrix[2][0] * old_ctm[0][0] + rot_matrix[2][2] * old_ctm[2][0]
    new_ctm[2][2] = rot_matrix[2][0] * old_ctm[0][2] + rot_matrix[2][2] * old_ctm[2][2]
    #stack.append(new_ctm)
    stack[len(stack) - 1] = new_ctm

def gtRotateZ(theta):
    # Convert degrees to radians
    rad = radians(theta)
    # Make z rotation matrix
    rot_matrix = [[0 for i in range(4)] for j in range(4)]
    rot_matrix[0][0] = cos(rad)
    rot_matrix[0][1] = -1.0 * sin(rad)
    rot_matrix[1][0] = sin(rad)
    rot_matrix[1][1] = cos(rad)
    rot_matrix[2][2] = 1.0
    rot_matrix[3][3] = 1.0
    # Get old ctm
    old_ctm = stack[len(stack) - 1]
    # Deep copy old to new ctm
    new_ctm = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            new_ctm[i][j] = old_ctm[i][j]
    new_ctm[0][0] = rot_matrix[0][0] * old_ctm[0][0] + rot_matrix[0][1] * old_ctm[1][0]
    new_ctm[0][1] = rot_matrix[0][0] * old_ctm[0][1] + rot_matrix[0][1] * old_ctm[1][1]
    new_ctm[1][0] = rot_matrix[1][0] * old_ctm[0][0] + rot_matrix[1][1] * old_ctm[1][0]
    new_ctm[1][1] = rot_matrix[1][0] * old_ctm[0][1] + rot_matrix[1][1] * old_ctm[1][1]
    #stack.append(new_ctm)
    stack[len(stack) - 1] = new_ctm

def print_ctm():
    ctm = stack[len(stack) - 1]
    for i in range(4):
        print ctm[i]
    print "\n"