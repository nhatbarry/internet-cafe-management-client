
from pymongo.mongo_client import MongoClient
import sys
import os
from mainWindowApp import MainWindowApp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loginUi4.loginUi4 import Ui_Form
from PyQt5 import QtWidgets


uri = 'mongodb+srv://nhatbarry_db_user:A5fvCiLouoY0yFWi@cluster0.g42qlnp.mongodb.net/?appName=Cluster0'

class LoginApp(QtWidgets.QWidget, Ui_Form): 
    
    def __init__(self, *args, **kwargs):
        super(LoginApp, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.checkUser)

    def checkUser(self):
        client = MongoClient(uri)
        db = client.internet_cafe
        col = db.users
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        
        query = col.find_one({'username': username, 'password': password})
        if query:
            self.mainWindow = MainWindowApp()
            self.mainWindow.show()
            self.close()
        else:
            print('nhot roi')

