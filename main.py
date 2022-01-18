from PixelField import *
from time import sleep
import math

MandelbrotMenge = PixelField(1000,1000, "white")
pixel = MandelbrotMenge.getPixelField()
MandelbrotMenge.setPixelField(pixel)
MandelbrotMenge.showPixelField()
MandelbrotMenge.putMandelbrotPixel()
MandelbrotMenge.setAssociatedComplex(-2, 3, 1.5, 3)

for i in range(0, 20):
    for rows in range(0, MandelbrotMenge.yRange):
        for cols in range(0, MandelbrotMenge.xRange):
                MandelbrotMenge.MandelbrotPixelField[rows][cols].calcIterationStep()
         
for rows in range(0, MandelbrotMenge.yRange):
    for cols in range(0, MandelbrotMenge.xRange):
        if MandelbrotMenge.MandelbrotPixelField[rows][cols].isPartOfSet:
            pixel[rows][cols] = (0,0,0)
        else:
            pixel[rows][cols] = (int(0.7*5*MandelbrotMenge.MandelbrotPixelField[rows][cols].cnt), int(0.8*5*MandelbrotMenge.MandelbrotPixelField[rows][cols].cnt), int(0.9*5*MandelbrotMenge.MandelbrotPixelField[rows][cols].cnt))

            
MandelbrotMenge.setPixelField(pixel)
MandelbrotMenge.updatePixelField()
sleep(3)
)
'''