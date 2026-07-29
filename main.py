import sys

from PySide6.QtWidgets import QApplication

from auth.auth_manager import AuthenticationManager
from ui.login_window import LoginWindow
from ui.register_window import RegisterWindow


app = QApplication(sys.argv)

auth = AuthenticationManager()

if auth.user_exists():
    window = LoginWindow()
else:
    window = RegisterWindow()

window.show()

sys.exit(app.exec())

