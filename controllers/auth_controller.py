from PyQt5.QtCore import pyqtSignal

from controllers.base_controller import BaseController
from models.user_model import UserModel


class AuthController(BaseController):  
    login_success = pyqtSignal(dict)
    login_failed = pyqtSignal(str) 
    logout_completed = pyqtSignal()
    
    def __init__(self, parent=None):
        super(AuthController, self).__init__(parent)
        self.user_model = UserModel()
        self.current_user = None
        
    def login(self, username: str, password: str):
        self.log(f"Đang xác thực user: {username}")
        
        if not username or not password:
            self.login_failed.emit("Vui lòng nhập đầy đủ thông tin!")
            return
            
        user = self.user_model.authenticate(username, password)
        
        if user:
            self.current_user = user
            self.log(f"Đăng nhập thành công: {username}")
            self.login_success.emit(user)
        else:
            self.log(f"Đăng nhập thất bại: {username}")
            self.login_failed.emit("Tên đăng nhập hoặc mật khẩu không đúng!")
            
    def logout(self):
        self.log("Đăng xuất")
        self.current_user = None
        self.logout_completed.emit()
        
    def get_current_user(self) -> dict:
        return self.current_user
        
    def is_authenticated(self) -> bool:
        return self.current_user is not None
