from PIL import Image
import subprocess
import os
import signal
import math




class MandelbrotPixel:
    def __init__(self, Real=0, Imag=0, absolutAmount = 0, cnt = 0):
        self.associatedReal = 0 # auf private setzen 
        self.associatedImag = 0
        self.Real = 0
        self.Imag = 0
        self.absolutAmount = 0
        self.cnt = 0
        self.isPartOfSet = True

    def calcIterationStep(self):
        if not self.cnt and self.isPartOfSet == True:
            self.Real = self.associatedReal
            self.Imag = self.associatedImag
            self.cnt+=1
            self.calculateAbsolutAmount()
        elif self.isPartOfSet:
            self.calcNewComplex()
            self.calculateAbsolutAmount()
        
    def calculateAbsolutAmount(self):
        self.absolutAmount = math.sqrt(pow(self.Real,2) + pow(self.Imag,2))
        if self.absolutAmount < 2:
            self.cnt+=1
        else:
            self.isPartOfSet = False

    def calcNewComplex(self):
        Real = self.Real 
        Imag = self.Imag 
        self.Real = math.pow(Real,2) - math.pow(Imag,2)
        self.Imag = 2 * Real * Imag
        self.Real = self.Real + self.associatedReal
        self.Imag = self.Imag + self.associatedImag


class PixelField:
    def __init__ (self, xRange, yRange, background="white", name="Mandelbrotset.png", processGroup = 0):
        self.xRange = xRange
        self.yRange = yRange
        self.background = background
        self.ImagePath = "/home/cvend/Schreibtisch/Python_Uebungen/Mandelbrotset/" + name
        self.ImageSet = Image.new( 'RGB', (self.xRange,self.yRange), self.background)
        self.ImageSet.save(self.ImagePath)
        self.processGroup = processGroup
        self.MandelbrotPixelField = []


    def putMandelbrotPixel(self):
        rows = []
        for x in range(0, self.yRange): # Formatieren der Liste zur weitern Bearbeitung
            for y in range(0, self.xRange):
                rows.append(MandelbrotPixel())        
            self.MandelbrotPixelField.append(rows)
            #print(rows)
            rows = []
        
    def setAssociatedComplex(self, realStart, realRange, imagStart, imagRange):
        realRes =  realRange / self.xRange
        imagRes = imagRange / self.yRange

        for rows in range(0, self.yRange):
            for cols in range(0, self.xRange):
                self.MandelbrotPixelField[rows][cols].associatedReal = realStart + realRes * cols
                self.MandelbrotPixelField[rows][cols].associatedImag = imagStart - imagRes * rows



    def showPixelField(self):
        self.processGroup = subprocess.Popen("eog " + self.ImagePath, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    def getPixelField(self): # holt die Pixel und formatiert sie zur weiteren Bearbeitung
        pixels = self.ImageSet.getdata()      
        rows = []
        Liste = []
        cnt = 0
        temp = []
        for k in range(0,len(pixels)): # Übertragen der Pixelwerte in Liste
            temp.append(pixels[k])

        for x in range(0, self.yRange): # Formatieren der Liste zur weitern Bearbeitung
            for y in range(0, self.xRange):
                rows.append(temp[cnt])
                cnt+=1
            Liste.append(rows)
            rows = []
        return Liste

    def getPixelFieldRaw(self):
        pixels = self.ImageSet.getdata()
        temp = []
        for k in range(0,len(pixels)): # Übertragen der Pixelwerte in Liste
            temp.append(pixels[k])
        return temp
        
    def calcSin(self):
        dataList = self.getPixelField()
        middle = int(self.yRange / 2) # "draw middle line"
        for cols in range(0, self.xRange):
            dataList[middle][cols] = (0,0,0)
        xRes = (2*math.pi) / self.xRange
        erg = []
        for x in range(0,self.xRange):
            y = math.sin(x*xRes) * (-1)
            y = int((middle-1)*y - middle)
            erg.append(y)
        for x in range(0, self.xRange):
            dataList[erg[x]][x] = (12,150,80)
        return dataList

    def setPixelField(self, pixelField):
        data = []
        for row in range(0, self.yRange):
            for col in range(0, self.xRange):
                data.append(pixelField[row][col])
        self.ImageSet.putdata(data)


    def setPixelFieldRaw(self, pixelField):
        self.ImageSet.putdata(pixelField)

    def updatePixelField(self):
        os.killpg(os.getpgid(self.processGroup.pid), signal.SIGTERM)
        self.ImageSet.save(self.ImagePath)
        self.processGroup = subprocess.Popen("eog " + self.ImagePath, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)


    def __del__(self):
        os.killpg(os.getpgid(self.processGroup.pid), signal.SIGTERM)
    
