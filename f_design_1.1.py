import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QSlider
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.uic import loadUi
import cv2, imutils
from pdf2image import convert_from_path
import numpy as np
from PIL import Image

#x1,y1,x2,y2 = input("Enter X1, Y1, X2 and Y2").split()
#x1= int(x1)
#x2= int(x2)
#y1= int(y1)
#y2= int(y2)
#
#print( x1, x2)

class GUICode(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # set the title
        self.setWindowTitle("")

        # setting window icon
        self.setWindowIcon(QIcon("logo.jpeg"))

        # setting icon text
        self.setWindowIconText("Focal-Design")
        loadUi('guiv1.ui',self)
        # geek list

        self.btn_browse.clicked.connect(self.onClick)
        
        self.btn_save.clicked.connect(self.savePhoto)
        self.btn_pdf.clicked.connect(self.savePdf)
        self.slider_rad.valueChanged.connect(self.setPerfoRadius)
        self.slider_area.valueChanged.connect(self.setPerfoArea)

    stylesheet= """
        imgLabel{
        background-image: url("logo.jpeg");
        background-repeat: no-repeat;
        background-position: center;
    """

    @pyqtSlot()
    def onClick(self):
        #self.text.setText(area )
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.img = cv2.imread(self.filename)
       # img = cv2.imread('two1.png')
        self.displayImage(self.img, 1)
        cv2.destroyAllWindows()

    def displayImage(self, img, window=1):
        self.tmp = img
        qformat = QImage.Format_Indexed8
        if len(self.img.shape) == 3:
            if self.img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
            img = QImage(self.img.data,
                               self.img.shape[1],
                               self.img.shape[0],
                               self.img.strides[0],  # <--- +++
                               qformat)
            img = img.rgbSwapped()
            self.imgLabel.setPixmap(QPixmap.fromImage(img))
            self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)
       # self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #self.btn_perfo.clicked.connect(self.setperfo(img))


    def savePhoto(self):
        """ This function will save the image"""
        # using a file dialog.

        filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
        cv2.imwrite(filename, self.tmp)
        print('Image saved as:', self.filename)

    def savePdf(self):
        img1 = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        pil_image=Image.fromarray(img1)
        pil_image.save(r'output.pdf')
        print('Image saved ')  


    def setPerfoRadius(self, radius_tick):
        x1=int(self.txtx1.toPlainText())
        x2=int(self.txtx2.toPlainText())
        y1=x1
        y2=x2
#        y1=int(self.txty1.toPlainText())
#        y2=int(self.txty2.toPlainText())
        #img=self.tmp
        self.img = cv2.imread(self.filename)
        self.displayImage(self.img, 1)
        cv2.destroyAllWindows()
#        cv2.rectangle(self.img,(x1,y1),(x2,y2),(255,255,255),2)
        
        area_content = self.slider_area.value()

        # Radius of circle
        # radius = input("Enter circle size in digit(0-100)")
        radius = float(radius_tick) / 10
        self.text_rad.setText(str(radius)+ " mm")


        print('Tick value:', radius_tick)
        # Blue color in BGR
        color = (255, 255, 255)
        radius = float(radius)
        if radius >= 1 and radius <=1.3:
            radius = 2
            thick = 2
        elif radius > 1.3 and radius <=1.5:
        	radius = 3
        	thick = 1
        elif radius > 1.5 and radius <2.0:
        	radius = 4
        	thick = 1
        elif radius >= 2.0 and radius <2.5:
        	radius = 4
        	thick = 2
        elif radius >= 2.5 and radius <=3.0:
        	radius = 5
        	thick = 1
        thickness = -1
        i = radius * 2
        ii = 10
        area =int(area_content)
        print('Area:', area)
        i = i+y1
        k=0
        #k=0
        # img = self.tmp
        #while i < self.img.shape[0]:
        while i < y2:
            if k%2 ==0:
                j=x1+(area+radius)//2 +(radius//2)
            else:
                j=x1+radius
            #while j < self.img.shape[1]:
            while j < x2:
                image = cv2.circle(self.img, (j, i), radius, color, thick, ii, 0)
                image = cv2.circle(self.img, (j, i), radius, color, thickness, ii, 0)
                #		image[i][j]=[211,211,211]
                #		image[i+1][j]=[211,211,211]
                #		image[i][j+1]=[211,211,211]
                #		image[i-1][j]=[211,211,211]
                #		image[i][j-1]=[211,211,211]
                #		image[i-1][j-1]=[211,211,211]
                j += area
            k += 1
            i+=area-(area//2)

        self.displayImage(image)

    def setPerfoArea(self, area_tick):
        
        x1=int(self.txtx1.toPlainText())
        x2=int(self.txtx2.toPlainText())
        y1=x1
        y2=x2
        self.img = cv2.imread(self.filename)
        self.displayImage(self.img, 1)
        cv2.destroyAllWindows()
        radius_tick=self.slider_rad.value()
#        cv2.rectangle(self.img,(x1,y1),(x2,y2),(255,255,255),2)
        

        radius = float(radius_tick) / 10
        print('Tick value:', radius_tick,"  radius:",radius)
        # Blue color in BGR
        color = (255, 255, 255)
        radius = float(radius)
        if radius >= 1 and radius <=1.3:
            radius = 2
            thick = 2
        elif radius > 1.3 and radius <=1.5:
        	radius = 3
        	thick = 1
        elif radius > 1.5 and radius <2.0:
        	radius = 4
        	thick = 1
        elif radius >= 2.0 and radius <2.5:
        	radius = 4
        	thick = 2
        elif radius >= 2.5 and radius <=3.0:
        	radius = 5
        	thick = 1
        thickness = -1
        i = radius * 2
        ii = 10
        area = int(area_tick)
        self.text_area.setText(str(area_tick) + ' %')
        print('Area:', area_tick)
        i=i+y1
        k=0
        #k=0
        # img = self.tmp
        #while i < self.img.shape[0]:
        while i < y2:
            if k%2 ==0:
                j=x1+(area+radius)//2 +(radius//2)
            else:
                j=x1+radius
            #while j < self.img.shape[1]:
            while j < x2:
                image = cv2.circle(self.img, (j, i), radius, color, thick, ii, 0)
                image = cv2.circle(self.img, (j, i), radius, color, thickness, ii, 0)
                #		image[i][j]=[211,211,211]
                #		image[i+1][j]=[211,211,211]
                #		image[i][j+1]=[211,211,211]
                #		image[i-1][j]=[211,211,211]
                #		image[i][j-1]=[211,211,211]
                #		image[i-1][j-1]=[211,211,211]
                j += area
            k += 1
            i+=area-(area//2)

        self.displayImage(image)


app =QApplication(sys.argv)
window = GUICode()
window.show()
sys.exit(app.exec_())
