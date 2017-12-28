# In the routine below, you should draw your initials in perspective
# Sean Lu

from matlib import *
from drawlib import *

def persp_initials():
    gtInitialize()
    gtPerspective (60, -100, 100)
    gtPushMatrix()
    gtTranslate(0, 0, -4)
    gtScale(0.25, 0.25, 0)
    gtRotateZ(10)
    gtRotateY(55)
    gtRotateX(20)
    initialSL()
    gtPopMatrix()
    
def initialSL():
    gtBeginShape()
    # S
    gtVertex(-0.25, 1, 0)
    gtVertex(-1.25, 1, 0)
    
    gtVertex(-1.25, 1, 0)
    gtVertex(-1.25, 0, 0)
    
    gtVertex(-1.25, 0, 0)
    gtVertex(-0.25, 0, 0)
    
    gtVertex(-0.25, 0, 0)
    gtVertex(-0.25, -1, 0)
    
    gtVertex(-0.25, -1, 0)
    gtVertex(-1.25, -1, 0)
    
    # L
    gtVertex(0.25, 1, 0)
    gtVertex(0.25, -1, 0)
    
    gtVertex(0.25, -1, 0)
    gtVertex(1.25, -1, 0)
    
    gtEndShape()
    