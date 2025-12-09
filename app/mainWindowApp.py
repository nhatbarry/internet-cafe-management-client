
from pymongo.mongo_client import MongoClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mainWindow.mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets

uri = 'mongodb+srv://nhatbarry_db_user:A5fvCiLouoY0yFWi@cluster0.g42qlnp.mongodb.net/?appName=Cluster0'



class MainWindowApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindowApp, self).__init__(*args, **kwargs)
        self.setupUi(self)