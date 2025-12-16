
from PyQt5 import QtWidgets, QtCore

from views.ui.login_ui import Ui_LoginForm


class LoginView(QtWidgets.QWidget, Ui_LoginForm):

    
    login_requested = QtCore.pyqtSignal(str, str)
    
    def __init__(self, parent=None):
        super(LoginView, self).__init__(parent)
        self.setupUi(self)
        self._connect_signals()
        
    def _connect_signals(self):
        self.pushButton.clicked.connect(self._on_login_clicked)
        
    def _on_login_clicked(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text()
        self.login_requested.emit(username, password)
        
    def get_credentials(self) -> tuple:
        return (self.lineEdit.text().strip(), self.lineEdit_2.text())
    
    def clear_fields(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        
    def show_error(self, message: str):
        QtWidgets.QMessageBox.warning(self, "Lỗi đăng nhập", message)
        
    def show_success(self, message: str):
        QtWidgets.QMessageBox.information(self, "Thành công", message)
