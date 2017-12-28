#Sean Lu
#CS 3451
#Project 0 Warm-Up
#8/25/2017

def setup():
    size(500, 500)
    
def draw():
    background(255, 255, 255)
    #Convert [0, 500] to [-2, 2]
    a = mouseX / 125.0 - 2.0
    b = mouseY / 125.0 - 2.0
    #Create imaginary vector from mouse coords
    vector = complex(a, b)
    fractal(0, complex(0, 0), vector)
    
#n is power
#v is vector used for recursive call
#baseV is mouse position vector used to calculate new vectors
def fractal(n, v, baseV):
    if (n < 10):
        x = v.real
        y = v.imag
        #Convert back to draw using [-3, 3] scale
        x = x * (500.0 / 6.0) + 3.0
        y = y * (500.0 / 6.0) + 3.0
        vnew = baseV ** n
        #Colors based on power
        if n == 0 or n == 10 or n == 5:
            fill(255, 0, 0)
        elif n == 1 or n == 9 or n == 6:
            fill(0, 255, 0)
        elif (n == 2 or n == 8 or n == 4):
            fill(0, 0, 255)
        else:
            fill(0, 255, 255)
        #Draw ellipse 
        ellipse(250 + x, 250 + y, 5, 5)
        #Recursive call using new calculated vectors
        fractal(n + 1, v + vnew, baseV)
        fractal(n + 1, v - vnew, baseV)
        
        