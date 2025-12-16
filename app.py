
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5 import QtWidgets

from controllers.main_controller import MainController


def main():
    app = QtWidgets.QApplication(sys.argv)
    
    try:
        from views.ui import res_login
        from views.ui import res_rc
    except ImportError as e:
        print(f"resources: {e}")
    
    controller = MainController()
    
    controller.start()
    
    exit_code = app.exec_()
    
    controller.cleanup()
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
