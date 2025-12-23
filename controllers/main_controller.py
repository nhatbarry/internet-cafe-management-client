
import os
from PyQt5.QtCore import pyqtSignal

from controllers.base_controller import BaseController
from controllers.auth_controller import AuthController
from controllers.game_controller import Game_controller
from services.socket_service import ClientSocketService
from views.login_view import LoginView
from views.main_view import MainView
from views.ui import main_window


class MainController(BaseController):

    
    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)
        
        self.auth_controller = AuthController()
        self.game_controller = None
        
        self.socket_service = None
        
        self.login_view = None
        self.main_view = None
        
        self._setup_controllers()
        
    def _setup_controllers(self):
        self.auth_controller.login_success.connect(self._on_login_success)
        self.auth_controller.login_failed.connect(self._on_login_failed)
        self.auth_controller.logout_completed.connect(self._on_logout_completed)
        
    def start(self):
        self.log("Khởi động ứng dụng client")
        self._show_login()
        
    def _show_login(self):
        if self.login_view is None:
            self.login_view = LoginView()
            self.login_view.login_requested.connect(self._handle_login)
        self.login_view.show()
        
    def _handle_login(self, username: str, password: str):
        self.auth_controller.login(username, password)
        
    def _on_login_success(self, user: dict):
        self.log(f"Đăng nhập thành công: {user.get('username')}")
        
        if self.login_view:
            self.login_view.close()
            
        self._show_main_window(user)
        
        self._start_socket_service()
        
    def _on_login_failed(self, error: str):
        self.log(f"Đăng nhập thất bại: {error}")
        if self.login_view:
            self.login_view.show_error(error)
            
    def _on_logout_completed(self):
        self.log("Đã đăng xuất")
        
        if self.socket_service:
            self.socket_service.stop()
            self.socket_service = None
            
        if self.main_view:
            self.main_view.close()
            self.main_view = None
            
        self._show_login()
        
    def _show_main_window(self, user: dict = None):
        if self.main_view is None:
            self.main_view = MainView()
            self.game_controller = Game_controller(self.main_view)
            self._connect_main_view_signals()
        
        if user:
            self.main_view.set_user_info(user)
            
        self.main_view.show()
        
    def _connect_main_view_signals(self):
        self.main_view.logout_requested.connect(self._handle_logout)
        self.main_view.deposit_requested.connect(self._handle_deposit)
        self.main_view.change_password_requested.connect(self._handle_change_password)
        self.main_view.support_requested.connect(self._handle_support)
        self.main_view.closing.connect(self._handle_window_closing)
        
    def _handle_logout(self):
        if self.main_view.confirm_action("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self._save_user_data()
            self.auth_controller.logout()
            
    def _handle_deposit(self):
        self.log("Yêu cầu nạp tiền")
        self.main_view.show_notification("Nạp tiền", "Vui lòng liên hệ quản lý để nạp tiền!")
        
    def _handle_change_password(self):
        self.log("Yêu cầu đổi mật khẩu")
        
    def _handle_support(self):
        self.log("Yêu cầu hỗ trợ")
        self.main_view.show_notification("Hỗ trợ")
        
    def _start_socket_service(self):
        self.log("Khởi động socket service")
        self.socket_service = ClientSocketService()
        self.socket_service.command_received.connect(self._handle_server_command)
        self.socket_service.connection_status.connect(self._handle_connection_status)
        self.socket_service.start()
        
    def _handle_server_command(self, command: str):
        self.log(f"Nhận lệnh từ server: {command}")
        
        if command == "LOCK":
            self._lock_screen()
        elif command == "UNLOCK":
            self._unlock_screen()
        elif command == "SHUTDOWN":
            self._shutdown()
        elif command == "RESTART":
            self._restart()
        elif command.startswith("MESSAGE:"):
            message = command.replace("MESSAGE:", "")
            self.main_view.show_notification("Thông báo từ quản lý", message)
            
    def _handle_connection_status(self, connected: bool):
        status = "Đã kết nối" if connected else "Mất kết nối"
        self.log(f"Trạng thái kết nối: {status}")
        
    def _lock_screen(self):
        self.log("Khóa màn hình")
        
    def _unlock_screen(self):
        self.log("Mở khóa màn hình")
        
    def _shutdown(self):
        self.log("Tắt máy")
        
    def _restart(self):
        self.log("Khởi động lại")
    
    def _save_user_data(self):
        if not self.main_view or not self.main_view.current_user:
            return
        
        try:
            self.main_view.stop_timer()
            
            data_to_save = self.main_view.get_user_data_to_save()
            
            if data_to_save:
                username = self.main_view.current_user.get('username')
                
                from models.user_model import UserModel
                user_model = UserModel()
                success = user_model.update_user_by_username(username, data_to_save)
                
                if success:
                    self.log(f"Đã lưu dữ liệu user: {username}, số dư còn lại: {data_to_save.get('balance', 0):.0f} VND")
                else:
                    self.log(f"Không thể lưu dữ liệu user: {username}")
        except Exception as e:
            self.log(f"Lỗi khi lưu dữ liệu user: {e}")
    
    def _handle_window_closing(self):
        self.log("Đang đóng cửa sổ chính...")
        self._save_user_data()
        
    def cleanup(self):
        self._save_user_data()
        
        if self.socket_service:
            self.socket_service.stop()
