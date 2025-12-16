
import socket
import time
from PyQt5.QtCore import QThread, pyqtSignal

from config.settings import SERVER_IP, SERVER_PORT


class ClientSocketService(QThread):

    command_received = pyqtSignal(str)
    connection_status = pyqtSignal(bool)
    
    def __init__(self, manager_ip=None, port=None):
        super().__init__()
        self.manager_ip = manager_ip or SERVER_IP
        self.port = port or SERVER_PORT
        self.is_running = True
        self.client = None
        
    def run(self):
        while self.is_running:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print(f"Đang kết nối tới Manager {self.manager_ip}:{self.port}...")
                self.client.connect((self.manager_ip, self.port))
                print("Kết nối thành công!")
                self.connection_status.emit(True)
                
                while self.is_running:
                    try:
                        message = self.client.recv(1024).decode('utf-8')
                        if message:
                            print(f"Nhận lệnh: {message}")
                            self.command_received.emit(message)
                        else:
                            break
                    except socket.error:
                        break
                        
            except Exception as e:
                print(f"Lỗi kết nối: {e}. Thử lại sau 5s...")
                self.connection_status.emit(False)
                time.sleep(5) 
                
            finally:
                if self.client:
                    self.client.close()
                    
    def send_message(self, message: str):
        if self.client:
            try:
                self.client.send(message.encode('utf-8'))
                return True
            except socket.error as e:
                print(f"Lỗi gửi tin: {e}")
                return False
        return False
    
    def stop(self):
        self.is_running = False
        if self.client:
            self.client.close()
        self.quit()
        self.wait()
