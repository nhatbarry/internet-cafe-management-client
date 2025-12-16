
from PyQt5.QtCore import QObject


class BaseController(QObject):

    
    def __init__(self, parent=None):
        super(BaseController, self).__init__(parent)
        
    def log(self, message: str):
        print(f"[{self.__class__.__name__}] {message}")
