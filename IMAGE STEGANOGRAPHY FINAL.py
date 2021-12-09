import sys
from PyQt5 import QtWidgets, uic, QtCore,  QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import json
from json.decoder import JSONDecodeError
import maybe_final_rc
import requests_API as requests
import cv2 as cv
import numpy as np

global path_image1, path_image2, path_image3

class Login_Page(QDialog):
    def __init__(self):
        super(Login_Page,self).__init__()
        loadUi("first_Copy_Copy_Copy.ui",self)
        self.login_button.clicked.connect(self.loginfunction)
        self.signup1.clicked.connect(self.create)


    def loginfunction(self):
        username_1=self.username1.text()
        password_1=self.password1.text()
        if len(username_1)==0 or len(password_1)==0:
            self.invalid1.setText("⚠ PLEASE FILL UP THE FIELDS ⚠")
       
        elif len(username_1)>0 and len(password_1)>0:
            json_data={
                        'email':username_1,
                        'password':password_1
            }
            response=requests.login(json_data)

            if response['status']==200:
                menu=Menu()
                widget.addWidget(menu)
                widget.setCurrentIndex(widget.currentIndex()+1)
            
            elif response['status']==401:
                self.invalid1.setText(response['message'])
                self.invalid2.setText("(OR YOU ARE NOT WORTHYYYYY......)")

        
    def create(self):
        createacc=Createacc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Createacc(QDialog):
    def __init__(self):
        super(Createacc,self).__init__()
        loadUi("signup_Copy_Copy_Copy.ui",self)
        self.signup2.clicked.connect(self.createfunction)
        self.invalid2.setVisible(False)
        self.gotologin.setVisible(False)  


    def createfunction(self):
        username_2=self.username2.text()
        if self.password2.text()!=self.con_password.text():
            self.invalid2.setVisible(True)
            self.invalid2.setText("⚠ OOPS! SOMETHING IS WRONG ⚠")  
        elif len(username_2)==0 or len(self.password2.text())==0 or len(self.con_password.text())==0:
            self.invalid2.setVisible(True)
            self.invalid2.setText("⚠ PLEASE FILL UP THE FIELDS ⚠") 
        else:
            password_2=self.password2.text()
            json_data={
                        'email':username_2,
                        'password':password_2
            }
            response=requests.signup(json_data)

            if response['status']!=400:    
                self.invalid2.setVisible(True)
                self.invalid2.setText(response['message'])
                self.gotologin.setVisible(True)
                self.gotologin.clicked.connect(self.gotologinfunction)
            
            else:
                self.invalid2.setVisible(True)
                self.invalid2.setText(response['message']+"\n⚠ Please Enter A Strong Password ⚠")
                self.gotologin.setVisible(False)
             

    def gotologinfunction(self):
        login=Login_Page()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Menu(QDialog):
    def __init__(self):
        super(Menu,self).__init__()
        loadUi("menu_Copy_Copy_Copy.ui",self)
        self.encode_button.clicked.connect(self.encode)
        self.decode_button.clicked.connect(self.decode)
        self.logout.clicked.connect(self.log_out)
    

    def encode(self):
        encoder=Encoder()
        widget.addWidget(encoder)
        widget.setCurrentIndex(widget.currentIndex()+1)
    

    def decode(self):
        decoder=Decoder()
        widget.addWidget(decoder)
        widget.setCurrentIndex(widget.currentIndex()+1)
    

    def log_out(self):
        login=Login_Page()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Encoder(QDialog):
    def __init__(self):
        super(Encoder,self).__init__()
        loadUi("encoder_Copy_Copy_Copy.ui",self)
        self.encode_button.clicked.connect(self.encodefunction)
        self.browse_button_1.clicked.connect(self.get_img_file)
        self.browse_button_2.clicked.connect(self.get_save_file)
        self.return1.clicked.connect(self.mainmenu)
        
    
    def get_img_file(self):
        global path_image1
        path_image1=QFileDialog.getOpenFileName(self, 'Open file')
        self.browsed_img_1.setText(str(path_image1[0]))
        self.img_label.setPixmap(QPixmap(str(path_image1[0])))
    

    def get_save_file(self):
        global path_image2
        path_image2=QFileDialog.getSaveFileName(self, 'Save file','','Image Files (*.png)')
        self.saved_img.setText(str(path_image2[0]))


    def encodefunction(self):
        global path_image1, path_image2
        src=path_image1[0]
        #src=str(self.selected_img.currentText())
        #name_of_file=self.textEdit_2.toPlainText()
        text=self.textEdit.toPlainText()
        img=cv.imread(src,cv.IMREAD_UNCHANGED)
        text=text+"$"
        b=""
        for x in text:
            x=ord(x)
            answer=""
            while x>0:
                m=x%2
                answer=str(m)+answer
                x//=2
            while len(answer)<8:
                answer="0"+answer
            b=b+answer
        
        n=img.shape[0]
        m=img.shape[1]
        l=img.shape[2]
        textPointer=0
        done=0
        for i in range(0,n,1):
            for j in range(0,m,1):
                for k in range(0,l,1):
                    
                    im=1 if img[i][j][k]&1 else 0
                    
                    if b[textPointer]=='0':
                        if im==1:
                            img[i][j][k]-=1
                    else:
                        if im==0:
                            img[i][j][k]+=1
                    textPointer+=1
                    if textPointer==len(b):
                        done=1
                        break
                if done:
                    break
            if done:
                break
        
        cv.imwrite(path_image2[0],img)     
        #cv.imwrite('C:/Users/achar/Python Project (Image Steganography)/%s.png'%name_of_file,img)
        self.encode_success1.setText("ENCODING DONE SUCCESSFULLY")
        self.encode_success2.setText("ENCODED IMAGE IS STORED IN YOUR DEVICE")


    def mainmenu(self):
        menu=Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Decoder(QDialog):
    def __init__(self):
        super(Decoder,self).__init__()
        loadUi("decoder_Copy_Copy_Copy.ui",self)
        self.decode_button.clicked.connect(self.decodefunction)
        self.browse_button_1.clicked.connect(self.get_open_file)
        self.return2.clicked.connect(self.mainmenu)
    
    
    def get_open_file(self):
        global path_image3
        path_image3=QFileDialog.getOpenFileName(self, 'Open file')
        self.browsed_img_2.setText(str(path_image3[0]))
        self.img_label_2.setPixmap(QPixmap(str(path_image3[0])))


    def decodefunction(self):
        src=path_image3[0]
        img=cv.imread(src,cv.IMREAD_UNCHANGED)
        [n,m,l]=img.shape
        temp=""
        text=""
        done=0
        for i in range(0,n,1):
            for j in range(0,m,1):
                for k in range(0,l,1):
                    
                    im=1 if img[i][j][k]%2!=0 else 0

                    temp+=str(im)
                    if len(temp)==8:
                        q=8
                        power=(2**(q-1))
                        number=0
                        for s in temp:
                            number+=(power*(ord(s)-48))
                            power//=2
                        c=chr(number)
                        if c=='$':
                            done=1
                            break
                        
                        text+=c
                        temp=""
                if done:
                    break
            if done:
                break
        self.decoded_txt.setText(text)
        self.decode_success.setText("DECODING DONE SUCCESSFULLY")

    def mainmenu(self):
        menu=Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

app=QApplication(sys.argv)
mainwindow=Login_Page()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec_()

        