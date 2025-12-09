
import sys
import os
import loginApp, mainWindowApp

from PyQt5 import QtWidgets


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginForm = loginApp.LoginApp()
    loginForm.show()
    sys.exit(app.exec_())


