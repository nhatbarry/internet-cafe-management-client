
from PyQt5 import QtWidgets, QtCore

from views.ui.main_window import Ui_MainWindow



class MainView(QtWidgets.QMainWindow, Ui_MainWindow):
    
    logout_requested = QtCore.pyqtSignal()
    deposit_requested = QtCore.pyqtSignal()
    change_password_requested = QtCore.pyqtSignal()
    support_requested = QtCore.pyqtSignal()
    closing = QtCore.pyqtSignal() 
    
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_time)
        self.remaining_time = 0 
        self.initial_time = 0  
        self.price_per_hour = 5000  
        self.current_user = None  
        
        self.initial_size = self.size()
        self.initial_widget_geometries = {}
        self._save_initial_geometries()
        
        self.setMinimumSize(800, 600)
        
        self._connect_signals()
        
    def _connect_signals(self):
        self.logout_btn.clicked.connect(self.logout_requested.emit)
        self.deposit_btn.clicked.connect(self.deposit_requested.emit)
        self.changepwd_btn.clicked.connect(self.change_password_requested.emit)
        self.support_btn.clicked.connect(self.support_requested.emit)

    def set_user_info(self, user: dict):
        self.current_user = user
        
        username = user.get('username', 'N/A')
        self.username_lb.setText(username)
        
        balance = user.get('balance', 0)
        self.balance_text.setText(f"{balance:,.0f} VND")
        
        self.price_per_hour = user.get('price_per_hour', 5000)
        self.price_text.setText(f"{self.price_per_hour:,.0f} VND/h")
        
        if self.price_per_hour > 0:
            hours = balance / self.price_per_hour
            self.remaining_time = int(hours * 3600) 
            self.initial_time = self.remaining_time 
        else:
            self.remaining_time = 0
            self.initial_time = 0
        
        self._display_time_formatted()
        
        self.timer.start(1000)
    
    def _update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self._display_time_formatted()
        else:
            self.timer.stop()
            self.show_notification("Hết thời gian", "Thời gian sử dụng của bạn đã hết!")
    
    def _display_time_formatted(self):
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.time_lcd.display(time_str)
        
    def update_balance(self, balance: float):
        self.balance_text.setText(f"{balance:,.0f} VND")
        
    def display_time(self, remaining_time: int):
        self.remaining_time = remaining_time
        self._display_time_formatted()
    
    def stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
    
    def get_remaining_balance(self) -> float:
        if not self.current_user:
            return 0
        
        time_used = self.initial_time - self.remaining_time
        
        hours_used = time_used / 3600
        money_used = hours_used * self.price_per_hour
        
        initial_balance = self.current_user.get('balance', 0)
        
        remaining_balance = initial_balance - money_used
        
        return max(0, remaining_balance)
    
    def get_user_data_to_save(self) -> dict:
        if not self.current_user:
            return {}
        
        return {
            'balance': self.get_remaining_balance(),
            'remaining_time': self.remaining_time
        }
        
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
    
    def _save_initial_geometries(self):
        try:
            if hasattr(self, 'widget'):
                self.initial_widget_geometries['widget'] = self.widget.geometry()
            
            widgets_to_save = [
                'balls_game_btn', 'snake_btn', 'flappy_btn',
                'label', 'label_2', 'label_3',
                'label_4', 'deposit_btn', 'changepwd_btn',
                'support_btn', 'logout_btn', 'time_lcd',
                'label_5', 'label_6', 'label_7',
                'username_lb', 'balance_text', 'price_text'
            ]
            
            for widget_name in widgets_to_save:
                if hasattr(self, widget_name):
                    widget = getattr(self, widget_name)
                    self.initial_widget_geometries[widget_name] = widget.geometry()
        except Exception as e:
            print(f"Error saving geometries: {e}")
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        if not self.initial_widget_geometries:
            return
        
        try:
            width_ratio = self.width() / self.initial_size.width()
            height_ratio = self.height() / self.initial_size.height()
            
            if hasattr(self, 'tabWidget'):
                self.tabWidget.resize(
                    int(self.width()),
                    int(self.height())
                )
            
            for widget_name, initial_geom in self.initial_widget_geometries.items():
                if hasattr(self, widget_name):
                    widget = getattr(self, widget_name)
                    
                    new_x = int(initial_geom.x() * width_ratio)
                    new_y = int(initial_geom.y() * height_ratio)
                    new_width = int(initial_geom.width() * width_ratio)
                    new_height = int(initial_geom.height() * height_ratio)
                    
                    widget.setGeometry(new_x, new_y, new_width, new_height)
                    
                    if isinstance(widget, (QtWidgets.QLabel, QtWidgets.QPushButton)):
                        font = widget.font()
                        base_size = 13 if 'label' in widget_name.lower() else 10
                        new_font_size = max(8, int(base_size * min(width_ratio, height_ratio)))
                        font.setPointSize(new_font_size)
                        widget.setFont(font)
                    
                    elif isinstance(widget, QtWidgets.QTextEdit):
                        font = widget.font()
                        new_font_size = max(8, int(10 * min(width_ratio, height_ratio)))
                        font.setPointSize(new_font_size)
                        widget.setFont(font)
                    
                    elif isinstance(widget, QtWidgets.QLCDNumber):
                        widget.setDigitCount(8)
                        
        except Exception as e:
            print(f"Error in resizeEvent: {e}")
    
    def closeEvent(self, event):
        self.closing.emit()
        event.accept()
