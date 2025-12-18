import game
import sys
import os
import subprocess
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox

class Game_controller(QObject):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow

        self.game_list = {
            'balls_game_btn': 'game/bouncing_balls/game.py',
            'snake_btn': 'game/snake_game/game.py',
            'flappy_btn': 'game/flappy_bird/game.py'
        }


        self.initConnection()

    def initConnection(self):
        for btn_name, path in self.game_list.items():
            if hasattr(self.mainwindow, btn_name):
                btn = getattr(self.mainwindow, btn_name)
                btn.clicked.connect(lambda checked, path=path: self.launch(path))
    
    def launch(self, path):
        base_dir = os.getcwd()
        full_path = os.path.join(base_dir, path)
        game_folder = os.path.dirname(full_path)
        if not os.path.exists(full_path):
            QMessageBox.critical(self.mainwindow, "Lỗi", f"Không tìm thấy  game")
            return
        subprocess.Popen([sys.executable, full_path], cwd=game_folder)

