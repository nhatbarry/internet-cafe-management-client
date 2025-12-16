
from PyQt5 import QtWidgets, QtCore

from views.ui.main_window_ui import Ui_MainWindow


class MainView(QtWidgets.QMainWindow, Ui_MainWindow):
    
    logout_requested = QtCore.pyqtSignal()
    deposit_requested = QtCore.pyqtSignal()
    change_password_requested = QtCore.pyqtSignal()
    support_requested = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)
        self._connect_signals()
        
    def _connect_signals(self):
        self.pushButton_2.clicked.connect(self.logout_requested.emit)
        self.pushButton.clicked.connect(self.deposit_requested.emit)
        self.pushButton_3.clicked.connect(self.change_password_requested.emit)
        self.pushButton_4.clicked.connect(self.support_requested.emit)
        
    def update_balance(self, balance: float):
        self.lcdNumber.display(balance)
        
    def update_time(self, remaining_time: int):
        self.lcdNumber.display(remaining_time)
        
    def show_notification(self, title: str, message: str):
        QtWidgets.QMessageBox.information(self, title, message)
        
    def show_error(self, title: str, message: str):
        QtWidgets.QMessageBox.warning(self, title, message)
        
    def confirm_action(self, title: str, message: str) -> bool:
        reply = QtWidgets.QMessageBox.question(
            self, title, message,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        return reply == QtWidgets.QMessageBox.Yes
