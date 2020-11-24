from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QDesktopWidget, QDialog,QTabWidget
from PyQt5.QtWidgets import QComboBox, QCheckBox ,QGroupBox ,QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QDialogButtonBox, QListWidget, QStatusBar
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen
from PyQt5.QtCore import QDateTime, QTimer, pyqtSlot, QDate, QTime, QDateTime, Qt, QSize

import sys
import json
import paho.mqtt.client as mqtt
import ssl
import os.path

class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Broker")
        self.setWindowIcon(QIcon("icon.png"))

        vbox = QVBoxLayout()

        header = Header()
        tabWidget = QTabWidget()

        tabWidget.setFont(QtGui.QFont("Sanserif", 15))

        tabWidget.addTab(Broker(), "Connect to Broker")
        tabWidget.addTab(SetShadow(), "Set Shadow")
        tabWidget.addTab(ConnSettings(), "Broker Settings")

        vbox.addWidget(header)
        vbox.addWidget(tabWidget)

        self.setGeometry(300,300, 700, 700)
        self.center()
        self.setLayout(vbox)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class SetShadow(QWidget):
    def __init__(self):
        super().__init__()
        self.led1shad = ""
        self.led2shad = ""
        self.lamp1shad = ""
        self.lamp2shad = ""

        self.load_state()

        # Row Led 1
        led1Label = QLabel("LED 1: ")
        self.led1state = QPushButton()
        self.led1state.setFocusPolicy(Qt.NoFocus)
        self.led1state.setFixedSize(QtCore.QSize(70, 25))
        self.led1state.setText(self.led1shad)
        self.led1state.clicked.connect(self.on_click_led1)
        hbox1 = QHBoxLayout()
        hbox1.setContentsMargins(150, 0, 150, 10)
        hbox1.addWidget(led1Label)
        hbox1.addWidget(self.led1state)   

        # Row Led 2     
        led2label = QLabel("LED 2:")
        self.led2state = QPushButton()
        self.led2state.setFocusPolicy(Qt.NoFocus)
        self.led2state.setFixedSize(QtCore.QSize(70, 25))
        self.led2state.setText(self.led2shad)
        self.led2state.clicked.connect(self.on_click_led2)
        hbox2 = QHBoxLayout()
        hbox2.setContentsMargins(150, 0, 150, 10)
        hbox2.addWidget(led2label)
        hbox2.addWidget(self.led2state)   

        # Row Lamp 1
        lamp1label = QLabel("LAMP 1:")
        self.lamp1state = QPushButton()
        self.lamp1state.setFocusPolicy(Qt.NoFocus)
        self.lamp1state.setFixedSize(QtCore.QSize(70, 25))
        self.lamp1state.setText(self.lamp1shad)
        self.lamp1state.clicked.connect(self.on_click_lamp1)
        hbox3 = QHBoxLayout()
        hbox3.setContentsMargins(150, 0, 150, 10)
        hbox3.addWidget(lamp1label)
        hbox3.addWidget(self.lamp1state)  

        # Row Lamp 2 
        lamp2label = QLabel("LAMP 2:")
        self.lamp2state = QPushButton()
        self.lamp2state.setFocusPolicy(Qt.NoFocus)
        self.lamp2state.setFixedSize(QtCore.QSize(70, 25))
        self.lamp2state.setText(self.lamp2shad)
        self.lamp2state.clicked.connect(self.on_click_lamp2)
        hbox4 = QHBoxLayout()
        hbox4.setContentsMargins(150, 0, 150, 10)
        hbox4.addWidget(lamp2label)
        hbox4.addWidget(self.lamp2state) 

        # Confirm Button
        self.confirmState = QPushButton() 
        self.confirmState.setFocusPolicy(Qt.NoFocus)
        self.confirmState.clicked.connect(self.on_save_shadow)
        self.confirmState.setFixedSize(QtCore.QSize(150, 25))
        self.confirmState.setText("Save Shadow")
        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.confirmState)
        hbox5.setContentsMargins(150, 0, 150, 10)

        # Vertical Layout
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)

        groupBox = QGroupBox("Set thing Shadow")
        groupBox.setLayout(vbox)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)
        
        self.setLayout(mainLayout) 
    
    @pyqtSlot()
    def on_click_led1(self):
        if(self.led1state.text() == "OFF"):
            self.led1state.setText("ON")
            self.led1state.repaint()
        else:
            self.led1state.setText("OFF")
            self.led1state.repaint()
    
    def on_click_led2(self):
        if(self.led2state.text() == "OFF"):
            self.led2state.setText("ON")
            self.led2state.repaint()
        else:
            self.led2state.setText("OFF")
            self.led2state.repaint()

    def on_click_lamp1(self):
        if(self.lamp1state.text() == "OFF"):
            self.lamp1state.setText("ON")
            self.lamp1state.repaint()
        else:
            self.lamp1state.setText("OFF")
            self.lamp1state.repaint()

    def on_click_lamp2(self):
        if(self.lamp2state.text() == "OFF"):
            self.lamp2state.setText("ON")
            self.lamp2state.repaint()
        else:
            self.lamp2state.setText("OFF")
            self.lamp2state.repaint()

    def on_save_shadow(self):
        payload1 =  "{\"state\": {\"Led1\": \"" +  self.led1state.text() + "\", "
        payload2 = payload1 + " \"Led2\": \"" + self.led2state.text() + "\", "
        payload3 = payload2 + " \"Lamp1\": \"" + self.lamp1state.text() + "\", "
        payload = payload3 + " \"Lamp2\":\"" + self.lamp2state.text() + "\" }}"   
    
        print(payload)

        shadowfile = open("shadow.txt", "w")
        shadowfile.write(payload)
        shadowfile.close()

    def load_state(self):
        statefile = open("shadow.txt", "r")
        data = json.load(statefile)
        statefile.close()
        state = data["state"]
        self.led1shad = state["Led1"]
        self.led2shad = state["Led2"]
        self.lamp1shad = state["Lamp1"]
        self.lamp2shad = state["Lamp2"]

class Broker(QWidget):
    def __init__(self):
        super().__init__()

        settings_file = open("settings.txt", "r")
        settings = json.load(settings_file)
        settings_file.close()
        self.settings = settings["settings"]

        groupBox = QGroupBox("Connection to Broker")
        self.connectbtn = QPushButton()
        self.connectbtn.setFixedSize(QtCore.QSize(150, 25))
        self.connectbtn.setText("Connect")
        self.connectbtn.clicked.connect(self.on_click_connect)

        self.disconnectbtn = QPushButton()
        self.disconnectbtn.setFixedSize(QtCore.QSize(150, 25))
        self.disconnectbtn.setText("Disconnect")
        self.disconnectbtn.clicked.connect(self.on_click_disconnect)

        self.connectbtn.setEnabled(True)
        self.disconnectbtn.setEnabled(False)

        self.statuslabel = QLabel("Connection status: disconnected")
        self.statuslabel.setContentsMargins(0, 8, 0, 0)

        hbox = QHBoxLayout()
        hbox.addWidget(self.connectbtn)
        hbox.addStretch()
        hbox.addWidget(self.disconnectbtn)
        hbox.addStretch()
        hbox.addWidget(self.statuslabel)
        groupBox.setLayout(hbox)

        groupBox2 = QGroupBox("Log Events")
        self.LogBox = QListWidget()
        vboxp = QVBoxLayout() 
        vboxp.addWidget(self.LogBox)
        groupBox2.setLayout(vboxp)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(groupBox)
        mainLayout.addWidget(groupBox2)
        self.setLayout(mainLayout)

        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.tls_set("CA.pem", tls_version=ssl.PROTOCOL_TLSv1_2)

        self.mqttc.username_pw_set(self.settings["usr"], self.settings["psw"])

    def on_click_connect(self):
        print(self.settings["url"])
        self.mqttc.connect(self.settings["url"], int(self.settings["port"]), 60)
        self.mqttc.subscribe(self.settings["top1"], 0)
        self.mqttc.subscribe(self.settings["top2"], 0)
        self.mqttc.loop_start()

        self.statuslabel.setText("Connection status: connected")
        self.statuslabel.repaint()
        self.connectbtn.setEnabled(False)
        self.disconnectbtn.setEnabled(True)

    def on_click_disconnect(self):
        self.connectbtn.setEnabled(True)
        self.disconnectbtn.setEnabled(False)
        self.mqttc.loop_stop()
        self.mqttc.disconnect()
        self.statuslabel.setText("Connection status: disconnected")
        self.statuslabel.repaint()
        

    def on_connect(self, mqttc, obj, flags, rc):
        print("Connected, rc: " + str(rc))
        time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)[0:8]
        if rc == 0:
            self.LogBox.addItem(time + ": Connected, Result Code: " + str(rc) )
        else:
            self.LogBox.addItem(time + ": Not connected, Result Code: " + str(rc) )

        
    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)[0:8]

        shadow_file = open("shadow.txt", "r")
        shadow = shadow_file.read()
        shadow_file.close()

        # QUI, PUBLISH SHADOW 
        if(msg.topic == self.settings["top1"]):
            pubshad = mqttc.publish(self.settings["top3"], shadow, qos=0)
            self.LogBox.addItem(time + ": Publishing payload: ")
            self.LogBox.addItem("---> " + shadow)

        if(msg.topic == self.settings["top2"]):
            data = str(msg.payload)
            idx = len(data)
            self.LogBox.addItem(time + ": Received payload: ")
            self.LogBox.addItem("--->"  + data[2:idx-1])
            print(data[2:idx-1])
            
            

    def on_publish(self, mqttc, obj, mid):
        time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)[0:8]
        self.LogBox.addItem(time + ": Shadow published")

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)[0:8]
        self.LogBox.addItem(time + ": Subscribed, QOS: " + str(granted_qos)[1])
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def on_disconnect(self, mqttc, userdata, rc):
        time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)[0:8]
        self.LogBox.addItem(time + ": Disconnected from Broker, Result code: " + str(rc))
        print("Disconnected, rc: " + str(rc))

class ConnSettings(QWidget):
    def __init__(self):
        super().__init__()

        groupBox = QGroupBox("Broker settings")

        lab1 = QLabel("Broker URL:           ")
        lab2 = QLabel("Port:                 ")
        lab3 = QLabel("Username:             ")
        lab4 = QLabel("Password:             ")
        lab5 = QLabel("Get topic:            ")
        lab6 = QLabel("Update shadow topic:  ")
        lab7 = QLabel("Publish shadow topic: ")

        self.edit1 = QLineEdit()
        self.edit1.setMaximumWidth(350)
        self.edit2 = QLineEdit()
        self.edit2.setMaximumWidth(150)
        self.edit3 = QLineEdit()
        self.edit3.setMaximumWidth(350)
        self.edit4 = QLineEdit()
        self.edit4.setMaximumWidth(350)
        self.edit5 = QLineEdit()
        self.edit5.setMaximumWidth(350)
        self.edit6 = QLineEdit()
        self.edit6.setMaximumWidth(350)
        self.edit7 = QLineEdit()
        self.edit7.setMaximumWidth(350)

        saveConn = QPushButton()
        saveConn.setFocusPolicy(Qt.NoFocus)
        saveConn.setFixedSize(QtCore.QSize(250, 25))
        saveConn.setText("Save connection parameters")
        saveConn.clicked.connect(self.on_click_save)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(lab1)
        hbox1.addWidget(self.edit1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(lab2)
        hbox2.addWidget(self.edit2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(lab3)
        hbox3.addWidget(self.edit3)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(lab4)
        hbox4.addWidget(self.edit4)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(lab5)
        hbox5.addWidget(self.edit5)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(lab6)
        hbox6.addWidget(self.edit6)

        hbox7 = QHBoxLayout()
        hbox7.addWidget(lab7)
        hbox7.addWidget(self.edit7)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(saveConn)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox8)

        groupBox.setLayout(vbox)

        main = QVBoxLayout()
        main.addWidget(groupBox)
        
        self.setLayout(main)
    
    @pyqtSlot()
    def on_click_save(self):
        url = self.edit1.text()
        port = self.edit2.text()
        username = self.edit3.text()
        password = self.edit4.text()
        t1 = self.edit5.text()
        t2 = self.edit6.text()
        t3 = self.edit7.text()

        tmp1 =  "{ \"settings\" : { \"url\": \"" + url + "\", \"port\": \"" + port  + "\", \"usr\": \"" + username + "\", "
        tmp2 = tmp1 + "\"psw\": \"" + password + "\", \"top1\": \"" + t1 + "\", \"top2\": \"" + t2 + "\", \"top3\": \""
        settings_to_save = tmp2 + t3 + "\" }}"
        print(settings_to_save)

        with open("settings.txt", "w") as file:
            file.write(settings_to_save)

class Header(QWidget):
    def __init__(self):
        super().__init__()
        lbl1 = QLabel('Welcome back, Giovanni ', self)

        self.lbl2 = QLabel("                                                            ", self)        # Timer
        self.showTime()

        hbox = QHBoxLayout()
        hbox.addWidget(lbl1, Qt.AlignLeft)
        hbox.addWidget(self.lbl2)

        timer = QTimer(self) 
        timer.timeout.connect(self.showTime)                                                            # adding action to timer
        timer.start(1000)                                                                               # update the timer every second 

        self.setLayout(hbox)

    def showTime(self):                                                                                 # getting current time 
        time = QTime.currentTime()
        now = QDate.currentDate()
        self.lbl2.setText(time.toString(Qt.DefaultLocaleLongDate)[0:9] + "- " + now.toString(Qt.LocalDate)) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    tabdialog = Tab()
    tabdialog.show()
    app.exec()